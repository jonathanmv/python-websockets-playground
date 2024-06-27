#!/usr/bin/env python

import argparse
import asyncio
from datetime import datetime
import json
import random
import websockets
from common.logger import logger


def generate_book_ticker_message(symbol="ETHUSDT"):
    """
    Generates a synthetic message with the same structure as Binance bookTicker stream.
    """
    update_id = random.randint(1, 100000000000)  # random update ID
    # random bid price between 3000 and 3500
    bid_price = "{:.8f}".format(random.uniform(3000, 3500))
    # random bid quantity between 10 and 150
    bid_quantity = "{:.8f}".format(random.uniform(10, 150))
    # random ask price between 3000 and 3500
    ask_price = "{:.8f}".format(random.uniform(3000, 3500))
    # random ask quantity between 10 and 150
    ask_quantity = "{:.8f}".format(random.uniform(10, 150))

    message = {
        "u": update_id,
        "s": symbol,
        "b": bid_price,
        "B": bid_quantity,
        "a": ask_price,
        "A": ask_quantity
    }

    return json.dumps(message)


def generate_trade_message(symbol="ETHUSDT"):
    """
    Generates a synthetic message with the same structure as Binance trade streams.
    """
    event_type = "trade"
    # current timestamp in milliseconds
    event_time = int(datetime.now().timestamp() * 1000)
    trade_id = random.randint(1000000000, 2000000000)  # random trade ID
    # random price between 3000 and 3500
    price = "{:.8f}".format(random.uniform(3000, 3500))
    # random quantity between 0.01 and 1
    quantity = "{:.8f}".format(random.uniform(0.01, 1))
    # random trade time within the last second
    trade_time = event_time - random.randint(0, 1000)
    is_market_maker = random.choice([True, False])  # random boolean

    message = {
        "e": event_type,
        "E": event_time,
        "s": symbol,
        "t": trade_id,
        "p": price,
        "q": quantity,
        "T": trade_time,
        "m": is_market_maker,
        "M": True  # ignore
    }

    return json.dumps(message)


async def send_messages(websocket, symbol, messages_per_second, stream):
    while True:
        try:
            match stream:
                case "trade":
                    await websocket.send(generate_trade_message(symbol))
                case "bookTicker":
                    await websocket.send(generate_book_ticker_message(symbol))
                case _:
                    logger.error(f"Unsupported stream: {stream}")
                    raise ValueError(f"Unsupported stream: {stream}")
            await asyncio.sleep(1 / messages_per_second)
        except websockets.ConnectionClosed as e:
            logger.error(f"Connection closed with error: {e}")
            break


async def main(symbol: str, messages_per_second: int, stream: str):
    while True:
        try:
            logger.info("Connecting to ws://localhost:8765...")
            async with websockets.connect("ws://localhost:8765") as websocket:
                logger.info(f"Connected to ws://localhost:8765")
                await send_messages(websocket, symbol, messages_per_second, stream)
        except (websockets.ConnectionClosed, ConnectionRefusedError) as e:
            logger.error(f"Connection error: {e}")
            logger.info("Reconnecting in 1 seconds...")
            await asyncio.sleep(1)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Websockets producer")
    parser.add_argument("--symbol", type=str,
                        default="ETHUSD", help="Trade symbol to send messages for")
    parser.add_argument("--messages-per-second", type=int,
                        default=1, help="Number of messages to send per second")
    parser.add_argument("--stream", type=str,
                        default="trade", help="The stream to generate messages for (trade, bookTicker, kline, etc.). Different streams have different message formats.")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    asyncio.run(main(symbol=args.symbol,
                messages_per_second=args.messages_per_second,
                stream=args.stream))
