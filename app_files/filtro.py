from flask import render_template
from datetime import datetime
from sqlalchemy import func, and_

def exibirFiltroCustom(Tarefa, db, owner=None, filtrar_data_mais_proxima=False):
    context = {
        'datetime': datetime.utcnow(),
        'classes_de_tarefas': []
    }

    # exclui birthdays
    filtro_base = [Tarefa.intervalo_repeticao_mode != 'birthday']
    # se tem owner filtra por owner todas as tarefas
    if owner:
        filtro_base.append(Tarefa.owner == owner)

    # separa nas 5 classes (0 - 4)
    for classe in range(5):
        filtro_classe = filtro_base.copy()
        filtro_classe.append(Tarefa.classe == classe)

        # Determina a ordenação baseada em filtrar_data_mais_proxima
        if filtrar_data_mais_proxima:
            data_mais_proxima_da_classe = db.session.query(func.min(Tarefa.data_proxima)).filter(and_(*filtro_classe)).scalar()
            filtro_classe.append(Tarefa.data_proxima == data_mais_proxima_da_classe)
            order_by_clause = Tarefa.ordem.asc()
        else:
            # Ordena por data_proxima por padrão
            order_by_clause = Tarefa.data_proxima.asc()
        
        tarefas_da_classe = Tarefa.query.filter(and_(*filtro_classe)).order_by(order_by_clause).all()
        context['classes_de_tarefas'].append({'nome': str(classe), 'tarefas': tarefas_da_classe})

    # Adiciona a "classe" de aniversários, se não estiver filtrando por dono
    if not owner:
        filtro_aniversario = [Tarefa.intervalo_repeticao_mode == 'birthday']
        if filtrar_data_mais_proxima:
            data_mais_proxima_aniversarios = db.session.query(func.min(Tarefa.data_proxima)).filter(and_(*filtro_aniversario)).scalar()
            filtro_aniversario.append(Tarefa.data_proxima == data_mais_proxima_aniversarios)
            order_by_clause = Tarefa.ordem.asc()
        else:
            order_by_clause = Tarefa.data_proxima.asc()

        lista_aniversarios = Tarefa.query.filter(and_(*filtro_aniversario)).order_by(order_by_clause).all()
        context['classes_de_tarefas'].append({'nome': 'Aniversários', 'tarefas': lista_aniversarios})

    return render_template('index.html', **context)

