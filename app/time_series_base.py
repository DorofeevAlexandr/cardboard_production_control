import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("INFLUXDB_TOKEN")
org = "12"
url = "http://localhost:8086"
print(token)
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "ElectroCounters"

write_api = client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
    point = (
        Point("measurement1")
        .tag("client_name", "ABK")
        .field("energy", value)
    )
    write_api.write(bucket=bucket, org="12", record=point)
    time.sleep(1)  # separate points by 1 second
    print(value)
    print(point)

print('==================================================================')
query_api = client.query_api()

query = """from(bucket: "ElectroCounters")
 |> range(start: -100m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="12")

for table in tables:
  for record in table.records:
    print(record)
