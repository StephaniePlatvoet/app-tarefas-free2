from flask import redirect, url_for
from app_files.funcoes import calcular_proxima_data,is_data_no_passado

def feita(task_class,db,id):
    tarefa = task_class.query.filter_by(id=int(id)).first()

    intervalo_repeticao_mode = tarefa.intervalo_repeticao_mode
    intervalo_repeticao_value = tarefa.intervalo_repeticao_value
    proximo_domingo = tarefa.proximo_domingo
    data_proxima_na_bd = tarefa.data_proxima
    data_proxima_seguinte = tarefa.data_proxima_seguinte

    tarefa.data_proxima = data_proxima_seguinte
    tarefa.data_proxima_seguinte = calcular_proxima_data(data_proxima_seguinte,proximo_domingo,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = False)

    if intervalo_repeticao_mode == ('birthday') and not is_data_no_passado(data_proxima_na_bd):
        tarefa.data_proxima = data_proxima_na_bd
        tarefa.data_proxima_seguinte = data_proxima_seguinte


    db.session.commit()
    return redirect(url_for('go_home') + '#content')
