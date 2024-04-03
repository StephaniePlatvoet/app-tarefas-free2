from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import SU


def calcular_proxima_data(data,intervalo_repeticao_next_sunday,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = True):
    data_proxima = add_invervalo_tempo(data,intervalo_repeticao_mode,intervalo_repeticao_value,primeiraVez)

    if intervalo_repeticao_mode == 'specific_day_of_month':
        dia = int(intervalo_repeticao_value)
        data_proxima = proxima_data_specific_day_of_month(data,dia,primeiraVez)
    elif intervalo_repeticao_mode == ('specific_day_of_year'):
        dia,mes = intervalo_repeticao_value.split('-')[0], intervalo_repeticao_value.split('-')[1]
        data_proxima = proxima_data_specific_day_of_year(data,dia,mes,primeiraVez)
    elif intervalo_repeticao_mode == ('birthday'):
        dia,mes = intervalo_repeticao_value.split('-')[0], intervalo_repeticao_value.split('-')[1]
        data_proxima = proxima_data_specific_day_of_year(data,dia,mes,primeiraVez)
    elif intervalo_repeticao_mode in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        data_proxima = proxima_data_specific_week_day(data,intervalo_repeticao_mode,primeiraVez)
    # Find the next Sunday after the calculated date if requested
    data_proxima = find_the_next_Sunday(data_proxima,intervalo_repeticao_next_sunday,primeiraVez)
    return data_proxima

#for calcular_proxima_data
def find_the_next_Sunday(data,QuerEncontrar,primeiraVez,ProximoIncuindoHoje=False,domingoPassado=True,domingoDaquiAUmaSemana=False):
    # Find the next Sunday after the calculated date if requested
    data = data
    if data and QuerEncontrar:
        if ProximoIncuindoHoje or primeiraVez:
            data += relativedelta(weekday=SU)
        elif domingoPassado:
            data -= timedelta(days=6)
            data = data + relativedelta(weekday=SU)
        elif domingoDaquiAUmaSemana:
            data += timedelta(days=6)
            data = data + relativedelta(weekday=SU)

    return data
def is_data_no_passado(data):
    if data < datetime.today():
        return True
    return False
def proxima_data_specific_day_of_month(data,dia,primeiraVez):
    data = data.replace(day=int(dia))
    if primeiraVez:
        if is_data_no_passado(data):
            data = (data + relativedelta(months=1)).replace(day=int(dia)) # ex true: hoje(30.3.2024), data(20.3.2024) dá (20.4.2024)
    else:
        data = (data + relativedelta(months=1)).replace(day=int(dia)) # ex true: hoje(30.3.2024), data(20.3.2024) dá (20.4.2024)
    return data
def proxima_data_specific_day_of_year(data,dia,mes,primeiraVez):
    data = data.replace(month=int(mes), day=int(dia))
    if primeiraVez:
        if is_data_no_passado(data):
            data = data.replace(year=data.year + 1) # ex true: hoje(30.12.2024), data(20.1.2024) dá (20.1.2025)
    else:
        data = data.replace(year=data.year + 1) # ex true: hoje(30.12.2024), data(20.1.2024) dá (20.1.2025)
    return data
def proxima_data_specific_week_day(data,week_day,primeiraVez):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_index = weekdays.index(week_day)
    data_in = data
    data += relativedelta(weekday=weekday_index)
    if data == data_in and not primeiraVez:
        data += timedelta(days=7)
    return data
def add_invervalo_tempo(data,intervalo_repeticao_mode,intervalo_repeticao_value,primeiraVez):
    data_proxima = data
    if primeiraVez:
        data_proxima = data
    else:
        if intervalo_repeticao_mode == 'days':
            data_proxima = data + timedelta(days=int(intervalo_repeticao_value))
        elif intervalo_repeticao_mode == 'weeks':
            data_proxima = data + timedelta(weeks=int(intervalo_repeticao_value))
        elif intervalo_repeticao_mode == 'months':
            data_proxima = data + relativedelta(months=int(intervalo_repeticao_value))
        elif intervalo_repeticao_mode == 'years':
            data_proxima = data + relativedelta(years=int(intervalo_repeticao_value))
    return data_proxima

def custom_order(value):
    if not value:
        return None
    else:
        return int(value)
    
#for criar tarefa e import csv
def criarImport(task_class,db, descricao, feita, data_primeira_vez,data_proxima,data_proxima_seguinte, intervalo_repeticao_mode, intervalo_repeticao_value, proximo_domingo, classe, notas, ordem, owner):

    nova_tarefa = task_class(
        descricao=descricao,
        feita=feita,
        data_primeira_vez=data_primeira_vez,
        intervalo_repeticao_mode=intervalo_repeticao_mode,
        intervalo_repeticao_value=intervalo_repeticao_value,
        proximo_domingo=proximo_domingo,
        data_proxima=data_proxima,
        data_proxima_seguinte=data_proxima_seguinte,
        classe=classe,
        notas=notas,
        ordem=custom_order(ordem),
        owner=owner
    )

    db.session.add(nova_tarefa)
    db.session.commit()