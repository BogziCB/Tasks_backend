FROM python:3.12

RUN apt-get update

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code

EXPOSE 8080

CMD ["python", "main.py"]