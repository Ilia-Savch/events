FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/


COPY . /app/


CMD python manage.py migrate && python manage.py create_superuser && python manage.py runserver 0.0.0.0:8000