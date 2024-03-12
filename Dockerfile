FROM python:3.10.12

COPY requirements.txt /order_app/requirements.txt
WORKDIR /order_app
RUN pip install -r requirements.txt

COPY . /order_app

ENV FLASK_APP=order_app

WORKDIR /order_app/flask_app

# Раскомментировать при первом запуске
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD ["flask", "run", "--host=0.0.0.0"]