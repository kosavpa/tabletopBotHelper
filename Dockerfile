FROM python:3.12

ADD app /app/

RUN pip install -r /app/requirements.txt

CMD ["python", "/app/main.py"]