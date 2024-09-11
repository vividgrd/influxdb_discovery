import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# token = os.environ.get("INFLUXDB_TOKEN")
token = "6PFNrYQX2Lwd98sacBP3E5cjDOs1YlV-Bebf0IwowN9HQKKsjrJa4MpQX4M_Pvfvm19MmRqhGEIAfCurcjmzWA=="
org = "vividgrd"
url = "http://192.168.68.131:30003"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="pyBucket"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement2")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="vividgrd", record=point)
  time.sleep(1) # separate points by 1 second

