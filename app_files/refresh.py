from app_files.funcoes import is_data_no_passado, calcular_proxima_data
from flask import redirect,url_for

def refresh(Tarefa,db,classe_filter=None):
    if classe_filter == 'aniversarios':
        # Filtra especificamente pelos aniversários
        lista_de_tarefas = Tarefa.query.filter(Tarefa.intervalo_repeticao_mode == 'birthday').all()
    elif classe_filter is not None:
        # Filtra especificamente pela classe fornecida
        lista_de_tarefas = Tarefa.query.filter(Tarefa.classe == classe_filter, Tarefa.intervalo_repeticao_mode != 'birthday').all()
    else:
        # Filtra por todas as classes exceto a classe 0
        lista_de_tarefas = Tarefa.query.filter(Tarefa.classe != 0, Tarefa.intervalo_repeticao_mode != 'birthday').all()

    for tarefa in lista_de_tarefas:
        if is_data_no_passado(tarefa.data_proxima):
            while is_data_no_passado(tarefa.data_proxima):
                intervalo_repeticao_mode = tarefa.intervalo_repeticao_mode
                intervalo_repeticao_value = tarefa.intervalo_repeticao_value
                proximo_domingo = tarefa.proximo_domingo

                tarefa.data_proxima = tarefa.data_proxima_seguinte
                tarefa.data_proxima_seguinte = calcular_proxima_data(tarefa.data_proxima, proximo_domingo, intervalo_repeticao_value, intervalo_repeticao_mode, primeiraVez=False)

    db.session.commit()
    return redirect(url_for('go_home') + '#content')

