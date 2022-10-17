from typing import Dict
from client import InfluxClient
import json
import asyncio
from aiohttp import ClientSession, TCPConnector
from emulation import yield_fake_datum
from datetime import datetime


class App:
    def __init__(self, config: Dict, write_data: bool, verbose: bool = False) -> None:
        self.config = config
        self.client = InfluxClient(config)
        self.writer = self.client.writer
        self.keep_running = True
        self.write_data = write_data
        self.verbose = verbose
        self.bucket = self.config.get("INFLUX_BUCKET")
        self.ha_token = self.config.get("HA_REST_TOKEN")
        self.ha_endpoint = self.config.get("HA_REST_ENDPOINT")
        self.session = ClientSession(connector=TCPConnector(ssl=False))
        

    async def tear_down(self):
        print("Tearing down!")
        self.keep_running = False
        await self.client.tear_down()
        await self.session.close()


    async def get_sim_data(self) -> None:
        try:
            async for datum in yield_fake_datum():
                if self.verbose:
                    print(json.dumps(datum, indent=2))
                if self.write_data:
                    record = await self.client.transform_datum_into_influx_point(datum)
                    await self.write_point(self.bucket, record)
                    await self.post_to_ha(self.ha_token, self.ha_endpoint, datum)
        except asyncio.CancelledError:
            await self.tear_down()


    async def get_data(self) -> None:
        import drivers
        try:
            datum = await drivers.get_aggregate_sensor_datum(verbose=self.verbose, config=self.config)
            if self.write_data:
                record = await self.client.transform_datum_into_influx_point(datum)
                await self.write_point(self.bucket, record)
                await self.post_to_ha(self.ha_token, self.ha_endpoint, datum)
        except asyncio.CancelledError:
            await self.tear_down()


    async def run_sim(self):
        await self.get_sim_data()


    async def post_to_ha(self, token: str, endpoint: str, payload: Dict) -> None:
        headers = {
            "User-Agent": "pi_air_quality",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        payload["timestamp"] = timestamp

        datum = {
            "name": "Pi Air Quality Sensor",
            "state": "On",
            "attributes": payload
        }

        await self.session.post(
            url=endpoint,
            json=datum,
            headers=headers
        )


    async def write_point(self, bucket, record) -> None:
        await self.writer.write(bucket=bucket, record=record)


    async def run(self, is_simulation: bool) -> None:
        while self.keep_running:
            if is_simulation:
                await self.run_sim()
            else:
                await self.get_data()
