# Aleph Zero: Playground

TODO: Describe the thing...

## Simple Demo

```sh
./run.sh
```

Runs the playground server on port `12385`. Shares IPC with host.

## Two Node: Private IPC

Terminal 1:
```sh
./run.sh --name=foo -p 8000 --ipc=shareable
```

Terminal 2:
```sh
./run.sh --name=bar -p 8001 --ipc=container:foo
```

Runs two dockers, the first named has a playground on port `8000`, the second on port `8001`.
