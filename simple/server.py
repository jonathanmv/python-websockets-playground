#!/usr/bin/env python

import asyncio
import websockets
from websockets.server import serve
from common.logger import logger

CONNECTIONS = set()


async def register_connection(websocket):
    CONNECTIONS.add(websocket)
    logger.info(
        f"Connection from {websocket.remote_address}. Total connections: {len(CONNECTIONS)}")
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)
        logger.info(
            f"Connection from {websocket.remote_address} closed. Total connections: {len(CONNECTIONS)}")


async def listen_for_messages(websocket):
    logger.info(f"Listening for messages from {websocket.remote_address}")
    async for message in websocket:
        logger.info(
            f"Received: {message} from {websocket.remote_address}. Broadcasting...")
        websockets.broadcast(CONNECTIONS, message)


async def connection_handler(websocket):
    await asyncio.gather(
        register_connection(websocket),
        listen_for_messages(websocket)
    )


async def main():
    async with serve(connection_handler, "localhost", 8765):
        logger.info("Server listening on ws://localhost:8765")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
