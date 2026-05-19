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
    # token = os.environ.get("INFLUXDB_TOKEN")
    token = os.environ.get("TEST_SERVER_INFLUXDB_TOKEN")
    org = "12"
    # url = "http://influxdb:8086"
    # url = "http://127.0.0.1:8086"
    url = os.environ.get("TEST_SERVER_INFLUXDB_URL")
    # print(token)
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
    # print(r, g, b)
    # Форматируем в виде #RRGGBB
    return f"#{r:02X}{g:02X}{b:02X}"


def power_consumption(values):
    for cn in values:
        len_values = len(values[cn]['count_val'])
        for ind, val in enumerate(values[cn]['count_val']):
            if ind + 1 < len_values:
                next_val = values[cn]['count_val'][ind + 1]
            else:
                next_val = 0
            if val != 0 and next_val != 0:
                power_consumption = int(next_val - val)
                power_consumption = 0 if power_consumption > 10_000_000 else power_consumption
            else:
                power_consumption = 0
            values[cn]['count_val'][ind] = max(power_consumption, 0)



def get_times(time_start: dt.datetime, time_end:dt.datetime, step_minutes=60):
    times = []
    step_time = dt.timedelta(minutes=step_minutes)
    cur_time = time_start
    while cur_time < time_end:
        times.append(cur_time)
        cur_time = cur_time + step_time
    times.append(time_end)
    return times


def get_time_period(date: dt.date, data_reading_period='1 day'):
    time_start = dt.datetime(year=date.year,
                             month=date.month,
                             day=date.day,
                             hour=0,
                             minute=0,
                             second=0)
    if data_reading_period == '1 day':
        time_end = time_start +  dt.timedelta(days=1)
        time_start = time_start - dt.timedelta(hours=1)
    elif data_reading_period == '1 month':
        end_date = date + relativedelta(months=1)
        time_end = dt.datetime(year=end_date.year,
                                 month=end_date.month,
                                 day=end_date.day,
                                 hour=0,
                                 minute=0,
                                 second=0)
        time_start = time_start - dt.timedelta(days=1)
    else:
        time_end = time_start
    return time_start, time_end


def get_step_time(data_reading_period='1 day'):
    if data_reading_period == '1 day':
        return '1h'
    elif data_reading_period == '1 month':
        return '1d'
    else:
        return ''



def read_electro_counters_values(client, date: dt.date, data_reading_period='1 day'):
    org = "12"
    query_api = client.query_api()

    time_start, time_end = get_time_period(date, data_reading_period)
    st_step_time = get_step_time(data_reading_period)

    # time_start = time_start - dt.timedelta(hours=1)

    # t1 = get_times(time_start, time_end, step_minutes=60)
    # print(t1)
    st_time_start = f'{time_start.isoformat()}+03:00'
    st_time_end = f'{time_end.isoformat()}+03:00'

    query = f"""from(bucket: "ElectroCounters")    
     |> range(start: {st_time_start}, stop: {st_time_end})
     |> aggregateWindow(every: {st_step_time}, fn: max, createEmpty: false)
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
        measurement_time = (dt.datetime(year=record['_time'].year,
                                       month=record['_time'].month,
                                       day=record['_time'].day,
                                       hour=record['_time'].hour,
                                       minute=record['_time'].minute) +
                            dt.timedelta(hours=3))

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
