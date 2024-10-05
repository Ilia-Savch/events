FROM python:3.11

WORKDIR /app
COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD python manage.py migrate && python manage.py create_superuser && python manage.py runserver 0.0.0.0:8000