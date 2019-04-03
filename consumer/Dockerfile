FROM python:3.7-alpine3.9

COPY requirements.txt /requirements.txt
#RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY consumer.py /consumer.py

CMD ["python", "/consumer.py"]
