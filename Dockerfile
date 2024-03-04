FROM python:3.10.12

# Устанавливаем зависимости
COPY requirements.txt /order_app/requirements.txt
WORKDIR /order_app
RUN pip install -r requirements.txt

# Копируем файлы приложения
COPY . /order_app

# Устанавливаем переменную среды FLASK_APP
ENV FLASK_APP=order_app

WORKDIR /order_app/flask_app
# Создаем базу данных
# RUN flask shell -c "from flask_app import db; db.create_all()"
# RUN flask db create_all
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0"]