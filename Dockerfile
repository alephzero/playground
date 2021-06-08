FROM alpine:latest

RUN apk add --no-cache g++ git go linux-headers make python3-dev py3-pip
RUN python3 -m pip install -U pip

RUN mkdir -p /alephzero

# Install C-API
RUN cd /alephzero &&                                        \
    git clone https://github.com/alephzero/alephzero.git && \
    cd /alephzero/alephzero &&                              \
    make install -j

# Install Python-API
RUN cd /alephzero &&                                         \
    git clone https://github.com/alephzero/py.git &&         \
    cd /alephzero/py &&                                      \
    ln -s /alephzero/alephzero/* /alephzero/py/alephzero/ && \
    python3 -m pip install .

# Install Go-API
RUN go get github.com/alephzero/go

# Install Playground deps
RUN pip3 install aiohttp

WORKDIR /
COPY main.py /
COPY index.html /
COPY examples/ /examples/

CMD ["python3", "main.py"]
