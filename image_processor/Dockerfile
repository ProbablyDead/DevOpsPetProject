FROM python:3.12-alpine

WORKDIR /app/

COPY ./requirements.txt ./
RUN <<MLTL
    pip install --upgrade pip 
    pip install --no-cache-dir -r ./requirements.txt
MLTL

ADD ./ ./

ENTRYPOINT [ "python", "-m", "src" ]

