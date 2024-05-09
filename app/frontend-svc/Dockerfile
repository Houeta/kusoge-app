FROM python:alpine3.19

LABEL Owner="seppuku@duck.com"

EXPOSE 8080

WORKDIR /app

COPY . .

RUN pip install -r requirments.txt

ENTRYPOINT [ "python" ]
CMD [ "server.py" ]
