FROM alpine:3.10

RUN apk add python3
RUN pip3 install aiohttp

# TODO: install alephzero

COPY main.py /
COPY index.html /

CMD ["python3", "main.py"]
