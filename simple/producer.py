#!/usr/bin/env python

import argparse
import asyncio
import websockets
from common.logger import logger


async def send_messages(websocket, messages_per_second):
    counter = 0
    while True:
        try:
            logger.info("Sending 'Hello world!'...")
            await websocket.send("Hello world!")
            counter += 1
            logger.info(f"Sent {counter} messages")
            await asyncio.sleep(1 / messages_per_second)
        except websockets.ConnectionClosed as e:
            logger.error(f"Connection closed with error: {e}")
            break


async def main(messages_per_second: int = 1):
    while True:
        try:
            logger.info("Connecting to ws://localhost:8765...")
            async with websockets.connect("ws://localhost:8765") as websocket:
                await send_messages(websocket, messages_per_second)
        except (websockets.ConnectionClosed, ConnectionRefusedError) as e:
            logger.error(f"Connection error: {e}")
            logger.info("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Websockets producer")
    parser.add_argument("--messages-per-second", type=int,
                        default=1, help="Number of messages to send per second")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    asyncio.run(main(args.messages_per_second))
