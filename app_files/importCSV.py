import csv
from datetime import datetime
from app_files.funcoes import calcular_proxima_data,criarImport
from flask import Flask, request, redirect, url_for


def criar_tarefas(task_class,db,name_csv_file):
    with open(name_csv_file, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            descricao=row['\ufeffdescricao']
            feita=bool(int(row['feita']))
            data_primeira_vez_str=row['data_primeira_vez']
            intervalo_repeticao_mode=row['intervalo_repeticao_mode']
            intervalo_repeticao_value=row['intervalo_repeticao_value']
            proximo_domingo=bool(int(row['proximo_domingo']))
            classe=row['classe']
            notas=row['notas']
            ordem=row['ordem']
            owner=row['owner']
            data_primeira_vez = datetime.strptime(data_primeira_vez_str, '%Y-%m-%d') if data_primeira_vez_str else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            print(descricao,type(descricao))
            print(intervalo_repeticao_mode,type(intervalo_repeticao_mode))
            print(data_primeira_vez,type(data_primeira_vez))
            data_proxima = calcular_proxima_data(data_primeira_vez,proximo_domingo,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = True)
            print(data_proxima)
            data_proxima_seguinte = calcular_proxima_data(data_proxima, proximo_domingo, intervalo_repeticao_value, intervalo_repeticao_mode, primeiraVez=False)
            print(data_proxima_seguinte)
            criarImport(task_class,db, descricao, feita, data_primeira_vez,data_proxima,data_proxima_seguinte, intervalo_repeticao_mode, intervalo_repeticao_value, proximo_domingo, classe, notas, ordem, owner)

    return redirect(url_for('home') + '#content')

