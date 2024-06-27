#!/usr/bin/env python

import asyncio
import websockets
from common.logger import logger


async def listen_forever():
    logger.info("Connecting to ws://localhost:8765...")
    counter = 0
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            logger.info("Waiting for message...")
            message = await websocket.recv()
            counter += 1
            logger.info(f"Received {counter}: {message}")


if __name__ == "__main__":
    asyncio.run(listen_forever())
