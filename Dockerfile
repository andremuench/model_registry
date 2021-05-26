FROM python:3.7-slim-buster

EXPOSE 80

RUN mkdir /app 
COPY pyproject.toml /app 
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY python /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]