FROM python:alpine3.19 AS builder

RUN apk update && \
    apk add libpq-dev gcc musl-dev

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirments.txt .

RUN pip install -r requirments.txt

##########

FROM python:alpine3.19

LABEL Owner="seppuku@duck.com"

EXPOSE 5000

RUN apk update && \
    apk add libpq-dev

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY . .

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
