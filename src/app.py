from typing import Dict
from client import InfluxClient
import json
import asyncio
from emulation import yield_fake_datum


class App:
    def __init__(self, config: Dict, write_data: bool, verbose: bool = False) -> None:
        self.config = config
        self.client = InfluxClient(config)
        self.writer = self.client.writer
        self.keep_running = True
        self.write_data = write_data
        self.verbose = verbose
        

    async def tear_down(self):
        print("Tearing down!")
        self.keep_running = False
        await self.client.tear_down()


    async def get_sim_data(self) -> None:
        try:
            async for datum in yield_fake_datum():
                if self.verbose:
                    print(json.dumps(datum, indent=2))
                if self.write_data:
                    bucket = self.config.get("INFLUX_BUCKET")
                    record = await self.client.transform_datum_into_influx_point(datum)
                    await self.write_point(bucket, record)
        except asyncio.CancelledError:
            await self.tear_down()


    async def get_data(self) -> None:
        import drivers
        try:
            datum = await drivers.get_aggregate_sensor_datum(verbose=self.verbose)
            if self.write_data:
                bucket = self.config.get("INFLUX_BUCKET")
                record = await self.client.transform_datum_into_influx_point(datum)
                await self.write_point(bucket, record)
        except asyncio.CancelledError:
            await self.tear_down()


    async def run_sim(self):
        await self.get_sim_data()


    async def write_point(self, bucket, record) -> None:
        await self.writer.write(bucket=bucket, record=record)


    async def run(self, is_simulation: bool) -> None:
        while self.keep_running:
            if is_simulation:
                await self.run_sim()
            else:
                await self.get_data()
