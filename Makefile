run-stream:
	python -u stream.py

run-processer:
	nohup python -u sweepy.py >processer.out 2>processer.err
