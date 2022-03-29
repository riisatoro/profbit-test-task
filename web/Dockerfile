FROM python:3.8

WORKDIR /web/
COPY . .

RUN ls

RUN pip install poetry
RUN poetry export -o requirements.txt
RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh
