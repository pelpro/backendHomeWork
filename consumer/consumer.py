#!/usr/bin/env python3
import pika
import sys
import time
import string
import logging
import smtplib

def send_email(adr, html):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('pelpro@yandex.ru', 'pass')
    BODY = "\r\n".join((
        "From: %s" % "pelpro@yandex.ru",
        "To: %s" % adr,
        "Subject: %s" % "Confirm your email",
        "",
        html
    ))
    server.sendmail("pelpro@yandex.ru", [adr], BODY)
    print("Send email: ", BODY, file=sys.stderr, flush = True)
    server.quit()


def consume(ch, method, properties, data):
    str = data.decode()
    adr, html = str.split('*')
    send_email(adr, html)


time.sleep(4)
credentials = pika.PlainCredentials('guest', 'guest')
parametrs = pika.ConnectionParameters('rabbitMQ',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parametrs)
channel = connection.channel()
channel.queue_declare(queue='valid')
print('Connection\n', file=sys.stderr, flush = True)
channel.basic_consume(consume, queue='valid', no_ack=True)
try:
    channel.start_consuming()
except Exception as e:
    #print('Connection problems in consumer\n', e, file=sys.stderr, flush = True)
    channel.stop_consuming()
