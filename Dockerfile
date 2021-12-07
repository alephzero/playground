FROM alpine:latest

RUN apk add --no-cache g++ git linux-headers make python3-dev py3-pip
RUN python3 -m pip install -U pip

RUN mkdir -p /alephzero

# Install C-API
RUN cd /alephzero &&                                        \
    git clone --recurse-submodules --depth=1 https://github.com/alephzero/alephzero.git && \
    cd /alephzero/alephzero &&                              \
    make install -j A0_EXT_NLOHMANN=1 A0_EXT_YYJSON=1

# Install Python-API
RUN cd /alephzero &&                                         \
    git clone --recurse-submodules --depth=1 https://github.com/alephzero/py.git &&         \
    cd /alephzero/py &&                                      \
    python3 -m pip install .

# Install Playground deps
RUN pip3 install aiohttp

WORKDIR /
COPY main.py /
COPY index.html /
COPY examples/ /examples/

CMD ["python3", "main.py"]
