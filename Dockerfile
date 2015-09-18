FROM ubuntu:14.04
MAINTAINER Noppanit Charassinvichai <noppanit.c@gmail.com>

# Update packages
RUN apt-get update -y

RUN apt-get install -y git

RUN apt-get install -y curl
# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
                ca-certificates \
                libsqlite3-0 \
                libssl1.0.0 \
                build-essential \
                git-core \
                curl \
		zlib1g-dev \
                libpcre3-dev \
		libc-ares-dev \
        && rm -rf /var/lib/apt/lists/*

ENV PYTHON_VERSION 2.7.10
ENV PYTHON_PIP_VERSION 7.1.0

# gpg: key 18ADD4FF: public key "Benjamin Peterson <benjamin@python.org>" imported
RUN gpg --keyserver pool.sks-keyservers.net --recv-keys C01E1CAD5EA2C4F0B8E3571504C367C218ADD4FF

RUN set -x \
        && buildDeps='libsqlite3-dev libssl-dev libncurses5-dev' \
        && apt-get update && apt-get install -y $buildDeps --no-install-recommends && rm -rf /var/lib/apt/lists/* \
        && mkdir -p /usr/src/python \
        && curl -SL "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
        && curl -SL "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz.asc" -o python.tar.xz.asc \
        && gpg --verify python.tar.xz.asc \
        && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
        && rm python.tar.xz* \
        && cd /usr/src/python \
        && ./configure --enable-shared --enable-unicode=ucs4 \
        && make -j$(nproc) \
        && make install \
        && ldconfig \
        && curl -SL 'https://bootstrap.pypa.io/get-pip.py' | python2 \
        && pip install --no-cache-dir --upgrade pip==$PYTHON_PIP_VERSION \
        && find /usr/local \
                \( -type d -a -name test -o -name tests \) \
                -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
                -exec rm -rf '{}' + \
        && apt-get purge -y --auto-remove $buildDeps \
        && rm -rf /usr/src/python

# install "virtualenv", since the vast majority of users of this image will want it
RUN pip install --no-cache-dir virtualenv

CMD ["python"]

RUN mkdir -p /home/ubuntu/sweepy

ADD . /home/ubuntu/sweepy

RUN pip install -r /home/ubuntu/sweepy/requirements.txt

RUN apt-get update && apt-get install -y openssh-server apache2 supervisor
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor

COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY config/streaming.conf /etc/supervisor/conf.d/streaming.conf
COPY config/sweepy.conf /etc/supervisor/conf.d/sweepy.conf

EXPOSE 22 80
CMD ["/usr/bin/supervisord"]
