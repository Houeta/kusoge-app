FROM python:alpine3.19

LABEL Owner="seppuku@duck.com"

EXPOSE 5000

WORKDIR /app

COPY . .

RUN apk update && \
    apk add libpq-dev gcc musl-dev

RUN pip install -r requirments.txt

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
