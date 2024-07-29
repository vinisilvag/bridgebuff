immortals:
	python3 ./client/client.py 127.0.0.1 5000 1 immortals-output.csv

top-meta:
	python3 ./client/client.py 127.0.0.1 5000 2 top-meta-output.csv

run-server:
	python3 ./server/server.py
