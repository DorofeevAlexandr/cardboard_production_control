from dotenv import load_dotenv
import os
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import SYNCHRONOUS


load_dotenv()
# token = os.environ.get("INFLUXDB_TOKEN")
token = os.environ.get("TEST_SERVER_INFLUXDB_TOKEN")

org = "12"
# url = "http://influxdb:8086"
# url = "http://127.0.0.1:8086"
url = os.environ.get("TEST_SERVER_INFLUXDB_URL")

bucket = 'ElectroCounters'
bucket = '12'
with InfluxDBClient(url=url, token=token, org=org, debug=False) as client:

    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    """
    Query: using csv library
    """
    csv_result = query_api.query_csv(f'from(bucket:"{bucket}") |> range(start: -100m)',
                                     dialect=Dialect(header=True, delimiter=",", comment_prefix="#", annotations=[],
                                                     date_time_format="RFC3339"))

    print('+++++++++++++++++++++++++++++')
    for csv_line in csv_result:
        print(csv_line)

    print()
    print()