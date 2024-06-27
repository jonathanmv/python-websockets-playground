# Binance Streams Simulator

In a terminal, start the server

```
python -m simple.server
```

## Producer

Simulates packages emitted by [Binance Trade Streams](https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#trade-streams)

In a terminal, start the producer

```
python -m trade.producer --symbol ETHUSDT --messages-per-second 3 --stream bookTicker
```

## Consumer

Listens to messages from Binance or the local producer

To read messages from **Binance** run

```
python -m trade.consumer --symbol ethusdt --stream bookTicker
```

To read messages produced locally run

```
python -m trade.consumer --local true
```
