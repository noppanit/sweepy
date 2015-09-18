run-stream:
	python -u stream.py

run-processer:
	nohup python -u sweepy.py >processer.out 2>processer.err &

build-docker:
	docker build -t sweepy .

run-container:
	docker run -d -P sweepy supervisord
