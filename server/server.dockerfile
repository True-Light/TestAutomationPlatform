FROM python:3.10
ENV HTTP_PROXY_SERVER http://192.168.1.6:7890

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt --proxy="${HTTP_PROXY_SERVER}"

ENV PORT 80

EXPOSE $PORT

COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh
COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

WORKDIR /app
ENV PYTHONPATH /app

CMD ["/start.sh"]
