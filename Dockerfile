FROM python:3.10-alpine
LABEL com.rabitech.org="Rabitech Solutions"
LABEL version="1.0.0"
LABEL desc="Simple recipe rest api"

ENV PYTHONBUFFERRED 1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
    # RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# USER appuser