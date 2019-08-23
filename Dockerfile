FROM alpine:3.10

RUN apk add --no-cache g++ git linux-headers make python3-dev

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

# Install Playground deps
RUN pip3 install aiohttp

WORKDIR /
COPY main.py /
COPY index.html /

CMD ["python3", "main.py"]
