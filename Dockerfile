FROM python:3.12

ADD app /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "-u", "/app/main.py"]