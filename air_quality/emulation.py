from numpy import arange
from asyncio import sleep

ranges = {
    'co2': [300, 600],
    'tvoc': [100, 300],
    'temperature': [10, 35],
    'pressure': [1000, 1060],
    'altitude': [0, 2000],
    'humidity': [0, 100],
    'pm1.0': [0, 3000],
    'pm2.5': [0, 3000],
    'pm10.0': [0, 3000],
    '0.3um': [0, 3000],
    '0.5um': [0, 3000] ,
    '1.0um': [0, 3000],
    '2.5um': [0, 3000],
    '5.0um': [0, 3000],
    '10.0um': [0, 3000],
}

async def generate_fake_data():
    fake_data = {}
    for key in ranges:
        fake_data[key] = {}
        start = ranges[key][0]
        stop = ranges[key][1]
        step = (stop - start) * 0.1
        data = arange(start, stop, step).tolist()
        data.extend(data[-2::-1])
        fake_data[key]["data"] = data
    return fake_data

async def yield_fake_datum():
    fake_data = await generate_fake_data()
    num_in_sequence = 0
    while True:
        fake_datum = {}
        try:
            for datum in fake_data:
                fake_datum[datum] = fake_data[datum]["data"][num_in_sequence]
            yield fake_datum
            num_in_sequence += 1
            await sleep(1)
        except (StopIteration, IndexError):
            num_in_sequence = 1 # Don't repeat first value


if __name__ == '__main__':
    while True:
        from time import sleep
        import json
        for datum in yield_fake_datum():
            print(json.dumps(datum, indent=2))
            sleep(1)
