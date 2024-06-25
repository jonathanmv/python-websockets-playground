# Simple websockets server, producer and consumer

Each of the commands below assumes you have your virtual environment activated. If not, run `python setup_env.py` from the root folder and then run `source ./.venv/bin/activate`.

Start the server

```sh
python -m simple.server
```

In a different terminal, start a consumer

```sh
python -m simple.consumer
```

In a different terminal, start a producer

```sh
python -m simple.producer --messages-per-second 10
```
