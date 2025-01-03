FROM python:3.12-alpine

WORKDIR /
COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

ADD ./ ./

EXPOSE 8080/tcp

ENTRYPOINT [ "python", "." ]

