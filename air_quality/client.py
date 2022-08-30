from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from typing import Any, Dict
from asyncio.exceptions import TimeoutError


Point = Dict[str, Any]

class InfluxClient:
    def __init__(self, config: Dict):
        url = config.get("INFLUXDB_V2_URL")
        token = config.get("INFLUXDB_V2_TOKEN")
        org = config.get("INFLUXDB_V2_ORG")
        self.client = InfluxDBClientAsync(url, token, org)
        self.writer = self.client.write_api()


    async def tear_down(self):
        await self.client.close()


    async def transform_datum_into_influx_point(self, datum: Dict) -> Point:
        point = {
            'measurement': 'airsensors',
            'tags': {
                'host': 'airsensors',
                'location': 'home'
            },
            'fields': datum
        }
        return point


    async def write(self, bucket: str, record: Point) -> None:
        try:
            await self.writer.write(bucket, record)
        except TimeoutError:
            print(f"Timeout occured while writing: {record}")
