import requests
from common import SpeedTest
import asyncio
import websockets
import time
from websockets.exceptions import ConnectionClosedOK
import random
import json
from pprint import pprint


def generate_random_data(num_bytes):
        return bytearray(random.getrandbits(8) for _ in range(num_bytes))


class MLabNDT(SpeedTest):

    label = "mlab_ndt"
    upload_size_bytes = 8192  

    def get_location(self):
        response = requests.get("https://locate.measurementlab.net/ndt_ssl?format=json")
        if response.status_code != 200:
            raise Exception()
        return response.json()['fqdn']

    async def test_download(self, base_url):
        download_url = "wss://{}/ndt/v7/download".format(base_url)
        total_bytes = 0
        measurement = None
        try:
            async with websockets.connect(download_url, subprotocols=["net.measurementlab.ndt.v7"]) as ws:
                start = time.time()
                prev_time = start
                max_time = start + 10
                while time.time() < max_time:
                    message = await ws.recv()
                    total_bytes += len(message)
                    now = time.time()
                    if now - prev_time > .25:
                        measurement = {"bytes": total_bytes, "elapsed": now - start}
                        prev_time = now
                else:
                    await ws.close()
                    raise ConnectionClosedOK(1000, 'Timeout')
        except ConnectionClosedOK:
            mbps =  measurement['bytes'] * 8 / 1e6 / measurement['elapsed']
            return mbps    
    
    async def test_upload(self, base_url):
        results = {
            "bytes_sent": 0,
            "messages": []
        }

        async def receive_messages(ws):
            async for message in ws:
                results['messages'].append(message)

        async def upload_data(ws):
            try:
                while True:
                    payload = generate_random_data(self.upload_size_bytes)
                    await ws.send(payload)
                    results['bytes_sent'] += self.upload_size_bytes
            except ConnectionClosedOK:
                return

        upload_url = "wss://{}/ndt/v7/upload".format(base_url)
        async with websockets.connect(upload_url, subprotocols=["net.measurementlab.ndt.v7"]) as ws:
            consumer_task = asyncio.ensure_future(
                receive_messages(ws))
            producer_task = asyncio.ensure_future(
                upload_data(ws))
            done, pending = await asyncio.wait(
                [consumer_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
        data = json.loads(results['messages'][-1])
        mbps = data['TCPInfo']['BytesReceived'] * 8 / 1e6 / (data['TCPInfo']['ElapsedTime'] / 1e6)
        latency = data['TCPInfo']['RTT'] / 1e3
        return mbps, latency

    
    def run_test(self):
        base_url = self.get_location()
        down_speed = asyncio.get_event_loop().run_until_complete(self.test_download(base_url))
        up_speed, latency = asyncio.get_event_loop().run_until_complete(self.test_upload(base_url))
        
        return (down_speed, up_speed, latency)
