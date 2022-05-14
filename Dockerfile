FROM python:3.10-alpine
LABEL com.rabitech.org="Rabitech Solutions"
LABEL version="1.0.0"
LABEL desc="Simple recipe rest api"

ENV PYTHONBUFFERRED 1

COPY requirements.txt requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip3 install -r requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
    # RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# USER appuser