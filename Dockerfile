FROM alpine:3.10

RUN apk add --no-cache g++ git go make python3-dev

RUN mkdir -p /alephzero

# Install C-API
RUN cd /alephzero &&                                        \
    git clone https://github.com/alephzero/alephzero.git && \
    cd /alephzero/alephzero &&                              \
    make install -j

# Install Python-API
RUN cd /alephzero &&                                 \
    git clone https://github.com/alephzero/py.git && \
    cd /alephzero/py &&                              \
    pip3 install -r requirements.txt &&              \
    python3 setup.py install

# Install Go-API
RUN go get github.com/alephzero/go

# Install Playground deps
RUN pip3 install aiohttp

WORKDIR /
COPY main.py /
COPY index.html /
COPY examples/ /examples/

CMD ["python3", "main.py"]
