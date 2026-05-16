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
                          'energy_indic': str(c.energy_indic / 1000),
                          'energy': str(c.energy / 1000),
                          })
    return res_counters


def client_influxdb():
    load_dotenv()
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "12"
    url = "http://influxdb:8086"
    # url = "http://127.0.0.1:8086"
    print(token)
    return influxdb_client.InfluxDBClient(url=url, token=token, org=org)


def generate_random_hex_color(const_collor_number=-1):
    if const_collor_number == 0:
         r, g, b = 200, 17, 34
    elif const_collor_number == 1:
        r, g, b = 50, 0, 150
    elif const_collor_number == 2:
        r, g, b = 43, 129, 48
    elif const_collor_number == 3:
        r, g, b = 137, 73, 161
    elif const_collor_number == 4:
        r, g, b = 242, 228, 57
    elif const_collor_number == 5:
        r, g, b = 83, 17, 34
    elif const_collor_number == 6:
        r, g, b = 122, 202, 173
    elif const_collor_number == 7:
        r, g, b = 174, 155, 22
    elif const_collor_number == 8:
        r, g, b = 198, 126, 172
    elif const_collor_number == 9:
        r, g, b = 26, 30, 31
    else:
        # Генерируем три случайных целых числа в диапазоне 0–255 для RGB
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
    print(r, g, b)
    # Форматируем в виде #RRGGBB
    return f"#{r:02X}{g:02X}{b:02X}"


def power_consumption(values):
    for cn in values:
        prev_val = 0
        # print(cn)
        for ind, val in enumerate(values[cn]['count_val']):
            # print(ind, val)
            if val != 0 and prev_val != 0:
                # val = float(val)
                power_consumption = int(val - prev_val)
                power_consumption = 0 if power_consumption > 10_000_000 else power_consumption
            else:
                power_consumption = 0
            prev_val = val
            values[cn]['count_val'][ind] = max(power_consumption, 0)
            # print(power_consumption)
            # print(values[cn]['count_val'])


def get_times(time_start: dt.datetime, time_end:dt.datetime, step_minutes=60):
    times = []
    step_time = dt.timedelta(minutes=step_minutes)
    cur_time = time_start
    while cur_time < time_end:
        times.append(cur_time)
        cur_time = cur_time + step_time
    times.append(time_end)
    return times


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
    # time_start = time_start - dt.timedelta(hours=1)

    # t1 = get_times(time_start, time_end, step_minutes=60)
    # print(t1)
    st_time_start = f'{time_start.isoformat()}Z'
    st_time_end = f'{time_end.isoformat()}Z'

    query = f"""from(bucket: "ElectroCounters")    
     |> range(start: {st_time_start}, stop: {st_time_end})
     |> aggregateWindow(every: 1h, fn: median, createEmpty: false)
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
        measurement_time = dt.time(hour=record['_time'].hour,
                       minute=record['_time'].minute)
        if measurement_time not in times.keys():
            times[measurement_time] = {}

        client_name = record['client_name']
        if client_name not in values.keys():
            values[client_name] = {'count_val' : [],
                                   'color' : generate_random_hex_color(const_collor_number=len(values)),
            }
            # print(client_name)

        values[client_name]['count_val'].append(record['_value'])

    power_consumption(values)

    # print(times)
    # print(values)
    return times, values


if __name__ == '__main__':
    print('--------------------')
    client = client_influxdb()
    read_electro_counters_values(client=client,
                                 date=dt.date.today())
