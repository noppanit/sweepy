run-stream:
	python -u stream.py

run-processer:
	nohup python -u sweepy.py >processer.out 2>processer.err &

build-docker:
	sudo docker build -t sweepy .

run-container:
	sudo docker run -d -P sweepy supervisord
