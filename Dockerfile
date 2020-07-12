FROM python:3.7

WORKDIR /app
COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh
CMD ./entrypoint.sh