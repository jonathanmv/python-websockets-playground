import asyncio
from app.config import get_config
from websockets import ConnectionClosed
from websockets.sync.client import connect
import json
import time
import pyshark
import os


config = get_config(os.getenv('ENV', 'development'))


# Dictionary to store packet timestamps
packet_timestamps = {}


def load_packet_timestamps(pcap_file, ssl_keylog_file):
    cap = pyshark.FileCapture(
        pcap_file, display_filter='websocket', sslkeylog_file=ssl_keylog_file)
    for packet in cap:
        if 'ethusdt' in packet.websocket.payload:
            packet_timestamps[packet.websocket.payload] = float(
                packet.sniff_timestamp)


async def listen(uri: str):
    async with connect(uri) as websocket:
        while True:
            try:
                start_time = time.time()
                message = await websocket.recv()
                data = json.loads(message)
                end_time = time.time()

                # Get the packet timestamp from the capture file
                packet_time = packet_timestamps.get(message, None)

                if packet_time:
                    latency = end_time - packet_time
                    print(f"""Symbol: {data['s']}, Best Bid Price: {data['b']}, Best Bid Qty:
                          {data['B']}, Best Ask Price: {data['a']}, Best Ask Qty: {data['A']}, Latency: {latency: .6f} seconds""")
                else:
                    print(f"""Symbol: {data['s']}, Best Bid Price: {data['b']}, Best Bid Qty:
                          {data['B']}, Best Ask Price: {data['a']}, Best Ask Qty: {data['A']}(Packet not found in capture)""")

            except ConnectionClosed:
                print("Connection closed, retrying...")
                await asyncio.sleep(1)
                continue
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(1)
                continue


def run_websocket_listener():
    # Load packet timestamps from capture file
    load_packet_timestamps(config.PCAP_FILE, config.SSL_KEYLOG_FILE)

    # Run the WebSocket listener
    asyncio.get_event_loop().run_until_complete(listen(config.WEBSOCKET_URI))
