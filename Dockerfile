FROM alpine:latest

COPY requirements.txt .
COPY cms /cms/
COPY root /root/

RUN apk update && \
    apk add --no-cache postgresql-client bash python3 python3-dev py3-pip postgresql-dev gcc python3-dev musl-dev \
    && pip3 install -r requirements.txt

WORKDIR /cms

VOLUME /var/articles

EXPOSE 8000

ENTRYPOINT ["/root/entrypoint.sh"]
