#!/bin/bash
cd "$(dirname "$0")"

docker build -t alephzero_playground .

opts="$(getopt -o n:p: -l name:,port:,ipc: --name "$0" -- "$@")"
eval set -- "$opts"

NAME=""
PORT=12385
IPC="--ipc=host"

while true
do
  case "$1" in
    -n|--name)
      NAME="--name $2"
      shift 2
      ;;
    -p|--port)
      PORT=$2
      shift 2
      ;;
    --ipc)
      IPC="--ipc=$2 --pid=$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      echo "Unknown flag: $1" >&2
      exit 1
      ;;
  esac
done

docker run                         \
  --rm                             \
  -it                              \
  $NAME                            \
  -p $PORT:12385                   \
  $IPC                             \
  -v ${PWD}/main.py:/main.py       \
  -v ${PWD}/index.html:/index.html \
  -v ${PWD}/examples:/examples     \
  alephzero_playground
