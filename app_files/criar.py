#pip install python-dateutil

from flask import Flask, request, redirect, url_for
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import SU
from app_files.funcoes import calcular_proxima_data, criarImport

def criar(task_class,db):

    intervalo_repeticao_mode = request.form.get('intervalo_repeticao_mode')
    intervalo_repeticao_value = request.form.get('intervalo_repeticao_value')
    intervalo_repeticao_next_sunday = request.form.get('intervalo_repeticao_next_sunday')
    data_primeira_vez_str = request.form['data_primeira_vez']
    data_primeira_vez = datetime.strptime(data_primeira_vez_str, '%Y-%m-%d') if data_primeira_vez_str else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    data_proxima = calcular_proxima_data(data_primeira_vez,intervalo_repeticao_next_sunday,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = True)
    data_proxima_seguinte = calcular_proxima_data(data_primeira_vez,intervalo_repeticao_next_sunday,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = False)
    #
    descricao=request.form['descricao_tarefa']
    feita=False
    classe = request.form.get('classe')
    notas = request.form['notas']
    ordem = request.form['ordem']
    owner = request.form['owner']
    proximo_domingo=bool(intervalo_repeticao_next_sunday)

    criarImport(task_class,db, descricao, feita, data_primeira_vez,data_proxima,data_proxima_seguinte, intervalo_repeticao_mode, intervalo_repeticao_value, proximo_domingo, classe, notas, ordem, owner)

    return redirect(url_for('go_home') + '#content')



'''
from flask import Flask, request, redirect, url_for
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import SU
from funcoes import calcular_proxima_data

def criar(task_class,db):

    intervalo_repeticao_mode = request.form.get('intervalo_repeticao_mode')
    intervalo_repeticao_value = request.form.get('intervalo_repeticao_value')
    intervalo_repeticao_next_sunday = request.form.get('intervalo_repeticao_next_sunday')
    data_primeira_vez_str = request.form['data_primeira_vez']
    data_primeira_vez = datetime.strptime(data_primeira_vez_str, '%Y-%m-%d') if data_primeira_vez_str else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    data_proxima = calcular_proxima_data(data_primeira_vez,intervalo_repeticao_next_sunday,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = True)
    data_proxima_seguinte = calcular_proxima_data((data_proxima + timedelta(days=1)),intervalo_repeticao_next_sunday,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = False)

    # Create a new task with the specified content, done state, repeat interval mode and value, and next occurrence date
    tarefa = task_class(
        descricao=request.form['descricao_tarefa'],
        feita=False,
        data_primeira_vez=data_primeira_vez,
        # data_criacao
        # data_alteracao
        intervalo_repeticao_mode=intervalo_repeticao_mode,
        intervalo_repeticao_value=intervalo_repeticao_value,
        proximo_domingo=bool(intervalo_repeticao_next_sunday),
        data_proxima=data_proxima,
        data_proxima_seguinte = data_proxima_seguinte,
        classe = request.form.get('classe'),
        notas = request.form['notas'],
        ordem = request.form['ordem'],
        owner = request.form['owner']
    )
    db.session.add(tarefa)
    db.session.commit()
    return redirect(url_for('home') + '#content')'''