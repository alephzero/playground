#!/bin/bash
cd "$(dirname "$0")"

docker build -t alephzero_playground .

docker run                         \
  --rm                             \
  -it                              \
  -v ${PWD}/main.py:/main.py       \
  -v ${PWD}/index.html:/index.html \
  -p 12385:12385                   \
  alephzero_playground
