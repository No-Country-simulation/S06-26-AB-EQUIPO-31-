run:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(msg)"

test:
	pytest tests/ -v

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt
