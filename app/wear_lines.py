from datetime import datetime

from models import ElectroCounters


COUNTER_SIMULATION = True


def get_counter_indicator_value(registers, address):
    try:
        if registers:
            w0 = registers[address + 0]
            w1 = registers[address + 1]
            return w0 * 65536 + w1
        return 0
    except:
        return 0


def read_electro_counters_update_in_base(session, counters_params, registers):
    for counter in counters_params:
        if COUNTER_SIMULATION:
            energy = datetime.now().second
        else:
            energy = get_counter_indicator_value(registers, counter['number'])


        energy_k = energy * counter['transformation_coefficient']
        update_counter_in_base(session,
                              counter_params=counter,
                              energy=energy_k)


def read_electro_counters_params_in_base(session):
    params = []
    counters = session.query(ElectroCounters).all()
    for counter in counters:
        params.append({
            'id' : counter.id,
            'number' : counter.number,
            'client_name' : counter.client_name,
            'address' : counter.address,
            'transformation_coefficient' : counter.transformation_coefficient,
            'energy' : counter.energy,
            })
    return sorted(params, key=lambda x: x['number'])



def update_counter_in_base(session, counter_params, energy=0):
    number = counter_params['number']
    counter = session.query(ElectroCounters).filter(ElectroCounters.number==number).first()
    if counter:
        counter.energy = energy
        counter.updated_dt = datetime.now()
    else:
        counter = ElectroCounters(line_number=counter_params['number'])
    session.add(counter)
    session.commit()
