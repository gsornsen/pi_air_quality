# pi_air_quality

## Description

TODO: Write this
## Environment Setup

The following command will set-up a basic environment with all the python dependencies required to run the app.

```bash
make environment
```

## Emulator

### Additional Environment Setup
1. Install additional development environment dependencies
    - ```bash
        make dev-deps
        ```
1. Follow [the instructions](https://docs.influxdata.com/influxdb/v2.4/install/) to install InfluxDB
1. Read the [InfluxDB QuickStart Guide](https://docs.influxdata.com/influxdb/v2.4/get-started/) and
    - Create an org
    - Create a bucket
    - Create a token with read/write privileges to your bucket in your org

1. Copy org, bucket, and token from previous step into `sim.env`
    - ```bash
        INFLUXDB_V2_TOKEN=""
        INFLUXDB_V2_URL="http://localhost:8086"
        INFLUXDB_V2_ORG=""
        INFLUX_BUCKET=""
        ```

### Running the Emulator

The following command will start the Influx server, emulate the hardware, and write simulated data into your local InfluxDB instance.

```bash
make emulator
```
