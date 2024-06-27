#!/usr/bin/env python

import argparse
import asyncio
import websockets
from common.logger import logger

BINANCE_STREAM_ROOT_URL = "wss://stream.binance.com:443"
LOCAL_STREAM_ROOT_URL = "ws://localhost:8765"


async def listen_forever(symbol: str, stream: str, local: bool):
    if local:
        url = f"{LOCAL_STREAM_ROOT_URL}"
    else:
        url = f"{BINANCE_STREAM_ROOT_URL}/ws/{symbol}@{stream}"

    logger.info(f"Connecting to {url}...")
    counter = 0
    async with websockets.connect(url) as websocket:
        logger.info("Connected")
        while True:
            message = await websocket.recv()
            counter += 1
            logger.info(f"Received {counter}: {message}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Binance Stream Websockets Consumer")
    parser.add_argument("--symbol", type=str,
                        default="ethusdt", help="Trade symbol to send messages for")
    parser.add_argument("--stream", type=str,
                        default="trade", help="The stream to connect to (trade, bookTicker, kline, etc.)")
    parser.add_argument("--local", type=bool,
                        default=False, help="Connect to local server instead of Binance stream")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    asyncio.run(listen_forever(symbol=args.symbol,
                stream=args.stream, local=args.local))
