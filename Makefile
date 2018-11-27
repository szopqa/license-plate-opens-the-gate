install:
	pip3 install flask_cors flask && pip3 install -r requirements.txt             
	
start:
	cd src && python3 __init__.py