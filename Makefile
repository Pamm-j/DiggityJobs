install:
	#install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt

devinstall:
	#install commands
		pip install --upgrade pip &&\
		pip install -r requirements.txt &&\
		pip install -r dev_requirements.txt

format:
	#format code
	black *.py
lint:
	#flake8 or #pylint
	pylint --disable=R,C --extension-pkg-whitelist='pydantic' *.py 
test:
	#test
	python3 -m pytest -vv --cov=main test_*.py
build:
	#build container
	docker build -t scholar-sync-auth-container .
run:
	#run app on uvicorn
	uvicorn main:app --host 0.0.0.0 --port 8001 --reload
deploy:
	#deploy
	docker build -t scholar-sync-auth-container .
	aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 577679806996.dkr.ecr.us-west-1.amazonaws.com
	docker build -t scholar-sync-auth-container .
	docker tag scholar-sync-auth-container:latest 577679806996.dkr.ecr.us-west-1.amazonaws.com/scholar-sync-auth-image:latest
	docker push 577679806996.dkr.ecr.us-west-1.amazonaws.com/scholar-sync-auth-image:latest

preflight: install format lint test

all: install format lint test deploy