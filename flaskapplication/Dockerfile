FROM python:3.7-alpine3.9

ADD requirements.txt /requirements.txt
#RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD first_app.py /first_app.py
ADD config.py /config.py
COPY web_app web_app
COPY migrations migrations
ENV FLASK_APP first_app.py
ADD run.sh /run.sh
EXPOSE 5000
RUN chmod +x /run.sh
CMD ["/bin/sh", "/run.sh"]

