
up:
	py -3.10 -m venv ../venv
	. ../venv/Scripts/activate
	pip install -r requirements.txt
	python test_tree/manage.py migrate
	python test_tree/manage.py createsuperuser
	python test_tree/manage.py runserver
