from flask import url_for,redirect
from app_files.funcoes import find_the_next_Sunday, calcular_proxima_data

def adiar(Tarefa,db,id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()

    if tarefa.data_proxima is not None:

        intervalo_repeticao_mode = tarefa.intervalo_repeticao_mode
        intervalo_repeticao_value = tarefa.intervalo_repeticao_value
        proximo_domingo = tarefa.proximo_domingo
        data_proxima_na_bd = tarefa.data_proxima
        data_proxima_seguinte = tarefa.data_proxima_seguinte

        tarefa.data_proxima = find_the_next_Sunday(data_proxima_na_bd,True,primeiraVez = False,ProximoIncuindoHoje=False,domingoPassado=False,domingoDaquiAUmaSemana=True)
        tarefa.data_proxima_seguinte = calcular_proxima_data(tarefa.data_proxima,proximo_domingo,intervalo_repeticao_value,intervalo_repeticao_mode,primeiraVez = False)

        if intervalo_repeticao_mode == ('birthday'):
            return redirect(url_for('home') + '#content')


    db.session.commit()
    return redirect(url_for('go_home') + '#content')