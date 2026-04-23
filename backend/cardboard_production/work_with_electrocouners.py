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
