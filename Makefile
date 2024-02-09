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
	
run:
	#run app on uvicorn
	uvicorn main:app --reload 

preflight: install format lint test

