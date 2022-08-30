import busio
import adafruit_sgp30
import adafruit_bme680
import board
from adafruit_pm25.i2c import PM25_I2C
from decorators import run_in_executor
from pprint import pprint
from pyopenweather.weather import Weather


i2c_bus = busio.I2C(board.SCL, board.SDA, frequency=100000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c_bus)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c_bus)
pm25 = PM25_I2C(i2c_bus)
weather = Weather()
# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
bme_temperature_offset = 5
# Be quiet by default
verbose = False


@run_in_executor
def get_sgp30_datum():
    equivalent_co2, total_voc = sgp30.iaq_measure()
    datum = {
        'co2': equivalent_co2,
        'tvoc': total_voc
    }
    return datum

@run_in_executor
def get_sgp30_baselines():
    co2_baseline, tvoc_baseline = sgp30.baseline_eCO2, sgp30.baseline_TVOC
    baselines = {
        'co2_baseline': co2_baseline,
        'tvoc_baseline': tvoc_baseline
    }
    return baselines

@run_in_executor
def get_bme680_datum():
    bme680.sea_level_pressure = weather.pressure
    temperature = (bme680.temperature + bme_temperature_offset)
    pressure = bme680.pressure
    humidity = bme680.humidity
    altitude = bme680.altitude
    datum = {
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity,
        'altitude': altitude
    }
    return datum

@run_in_executor
def get_pm25_datum():
    datum = {}
    try:
        raw_datum = pm25.read()
        datum = {
            'pm1.0': raw_datum['pm10 standard'],
            'pm2.5': raw_datum['pm25 standard'],
            'pm10.0': raw_datum['pm100 standard'],
            '0.3um': raw_datum['particles 03um'],
            '0.5um': raw_datum['particles 05um'],
            '1.0um': raw_datum['particles 10um'],
            '2.5um': raw_datum['particles 25um'],
            '5.0um': raw_datum['particles 50um'],
            '10.0um': raw_datum['particles 100um'],
        }
    except RuntimeError:
        print('PM25 Sensor had bad CRC Checksum')
    finally:
        return datum

async def get_aggregate_sensor_datum():
    sgp30_datum = await get_sgp30_datum()
    bme680_datum = await get_bme680_datum()
    pm25_datum = await get_pm25_datum()
    aggregate_datum = {**sgp30_datum, **bme680_datum, **pm25_datum}
    if verbose:
        pprint(aggregate_datum)
    return aggregate_datum
