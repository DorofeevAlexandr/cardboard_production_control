import datetime as dt
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random

from.models import ElectroCounters


def get_counters_from_base():
    res_counters = []
    counters = ElectroCounters.objects.order_by('number')
    for c in counters:
        res_counters.append({'number': c.number,
                          'client_name': c.client_name,
                          'address': c.address,
                          'transformation_coefficient': c.transformation_coefficient,
                          'energy_indic': c.energy_indic,
                          'energy': c.energy,
                          })
    return res_counters


def client_influxdb():
    load_dotenv()
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "12"
    # url = "http://influxdb:8086"
    url = "http://127.0.0.1:8086"
    print(token)
    return influxdb_client.InfluxDBClient(url=url, token=token, org=org)


def write_electro_counters_values(client, counters_params:list):
    bucket = "ElectroCounters"
    org = "12"
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for counter in counters_params:
        number = counter['number']
        client_name = counter['client_name']
        energy_indic = counter['energy_indic']
        energy_k = counter['energy']
        point = (
            Point(f"Counter_{number}")
            .tag("client_name", client_name)
            .field("energy_indic", energy_indic)
            .field("energy", energy_k)
            )

        write_api.write(bucket=bucket, org=org, record=point)
        print(point)



def generate_random_hex_color():
    # Генерируем три случайных целых числа в диапазоне 0–255 для RGB
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # Форматируем в виде #RRGGBB
    return f"#{r:02X}{g:02X}{b:02X}"

def read_electro_counters_values(client, date: dt.date, step_months=0):
    org = "12"
    query_api = client.query_api()
    if step_months != 0:
        end_date = date + relativedelta(months=step_months)
    dtime_1_days = dt.timedelta(days=1)
    time_start = dt.datetime(year=date.year,
                             month=date.month,
                             day=date.day,
                             hour=0,
                             minute=0,
                             second=0)
    time_end = time_start + dtime_1_days
    time_start = '2026-04-27T05:28:03Z'
    '''
     |> window(every: 3m)
     |> mean()
    '''
    # | > range({time_start}: {time_end})
    query = f"""from(bucket: "ElectroCounters")    
     |> range(start: {time_start}, stop: 2026-04-27T10:05:03Z)
     |> group(columns: ["_time"])
     |> filter(fn: (r) => r._field == "energy")"""
    print(query)


    tables = query_api.query(query, org=org)
    times = {}
    values = {}
    for table in tables:
      for record in table.records:
        # print('--------------')
        # print(record)
        # print(record['_time'], record['_field'], record['_value'])
        measurement_time = dt.time(hour=record['_time'].hour + 3,
                       minute=record['_time'].minute)
        if measurement_time not in times.keys():
            times[measurement_time] = {}

        client_name = record['client_name']
        if client_name not in values.keys():
            values[client_name] = {'count_val' : [],
                                   'color' : generate_random_hex_color(),
            }
            # print(client_name)

        values[client_name]['count_val'].append(record['_value'])

    for cn in values:
        prev_val = 0
        print(cn)
        for ind, val in enumerate(values[cn]['count_val']):
            if val != 0 and prev_val != 0:
                power_consumption = val - prev_val
            else:
                power_consumption = 0
            prev_val = val
            values[cn]['count_val'][ind] = power_consumption
    # print(times)
    # print(values)
    return times, values


if __name__ == '__main__':
    print('--------------------')
    client = client_influxdb()
    read_electro_counters_values(client=client,
                                 date=dt.date.today())
