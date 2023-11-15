import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUX_ORG = "tanmaya"
INFLUX_URL = "http://localhost:8086"
INFLUX_BUCKET="data-ingest"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
writer = write_client.write_api(write_options=SYNCHRONOUS)


def store_data_in_influxdb(data):
    # Connect to InfluxDB
    # Store the data in the appropriate format

    influx_client = influxdb_client.InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    writer = influx_client.write_api(write_options=SYNCHRONOUS)
    for value in range(5):
        point = (
            Point("measurement1")
            .tag("tagname1", "tagvalue1")
            .field("field1", value)
        )
        writer.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        time.sleep(1) # separate points by 1 second



   
# for value in range(5):
#   point = (
#     Point("measurement1")
#     .tag("tagname1", "tagvalue1")
#     .field("field1", value)
#   )
#   writer.write(bucket=bucket, org="tanmaya", record=point)
#   time.sleep(1) # separate points by 1 second

query_api = write_client.query_api()

# query = """from(bucket: "data-ingest")
#  |> range(start: -10m)
#  |> filter(fn: (r) => r._measurement == "measurement1")"""
# tables = query_api.query(query, org="tanmaya")

# for table in tables:
#   for record in table.records:
#     print(record)

query_api = write_client.query_api()

query = """from(bucket: "data-ingest")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="tanmaya")

for table in tables:
    for record in table.records:
        print(record)