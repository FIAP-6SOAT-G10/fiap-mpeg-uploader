FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8080

ARG MONGO_URL
ENV MONGO_URL=${MONGO_URL}

CMD ["python", "fiap_mpeg_uploader/__main__.py"]
