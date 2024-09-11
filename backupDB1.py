import json
from datetime import datetime, timedelta
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "<my-bucket>"
org = "<my-org>"
token = "<my-token>"

url = "http://192.168.68.128:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

todays_date = datetime.today().date()
# print(todays_date)
# Set the date we want to query from
query_date = datetime(2023, 11, 28)
# print(query_date)

while query_date.date() <= todays_date:
    print(f'Querying date from {query_date}')

    # Create the start and stop times for query day
    start_time = query_date.strftime('%Y-%m-%dT00:00:00Z')
    stop_time = (query_date + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')

    # Query script
    query_api = client.query_api()

    query = f'''
    from(bucket:"boathouse")
    |> range(start: {start_time}, stop: {stop_time})
    |> filter(fn:(r) => r._measurement == "pn107005")
    '''
    # query = 'from(bucket:"boathouse")\
    # |> range(start: -1m)\
    # |> filter(fn:(r) => r._measurement == "pn107005")\
    # |> limit(n: 10)'
    # # |> last()'#\

    json_list = []
    record_count = 0

    result = query_api.query(org=org, query=query)

    if result:
        measurements = {}
        for table in result:
            time = None
            for record in table.records:
                field = record.get_field()
                value = record.get_value()
                time = record.get_time()
                time_unix = int(time.timestamp() * 1000)

                if time_unix not in measurements:
                    measurements[time_unix] = {}

                measurements[time_unix][field] = value

        for timestamp, data in measurements.items():
            data["DT"] = timestamp
            json_list.append(data)
            record_count += 1

        json_output = json.dumps(json_list, indent=4)
        # print(json_output)
        print(f'{query_date}: Found {record_count} records')

        # Write the JSON data to a file
        datestr = query_date.strftime('%Y-%m-%d')
        filename = f'backup/{datestr}.json'
        with open(filename, 'w') as file:
            file.write(json_output)
            print(f"Written output to file {filename}")
    else:
        print(f'{query_date}: Nothing found for this day')

    query_date += timedelta(days=1)

