import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# token = os.environ.get("INFLUXDB_TOKEN")
token = "6PFNrYQX2Lwd98sacBP3E5cjDOs1YlV-Bebf0IwowN9HQKKsjrJa4MpQX4M_Pvfvm19MmRqhGEIAfCurcjmzWA=="
org = "vividgrd"
url = "http://192.168.68.131:30003"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="pyBucket"

query_api = client.query_api()

query = """from(bucket: "pyBucket")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement2")"""
tables = query_api.query(query, org="vividgrd")

for table in tables:
  for record in table.records:
    print(record)
