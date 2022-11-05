FROM python:alpine AS base

LABEL maintainer="Zachary Wilson"
LABEL maintainer.email="wilsonze@gmail.com"

ENV PYTHONUNBUFFERED 1
RUN apk --no-cache update && apk --no-cache add git libxslt-dev libxml2-dev gcc musl-dev libffi-dev

FROM base AS build
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
COPY . .
RUN pip install -e .

FROM build AS main
ENTRYPOINT [ "scrapy" ]
