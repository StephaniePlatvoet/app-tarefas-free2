from flask import request, url_for,redirect,flash
from datetime import datetime


def editar(Tarefa,db,id):
    tarefa = Tarefa.query.get_or_404(id)
    if tarefa:
        # Atualizar os campos da tarefa com os valores recebidos do formulário
        tarefa.descricao = request.form['descricao']
        tarefa.feita = 'feita' in request.form
        tarefa.notas = request.form['notas']
        tarefa.classe = request.form['classe']
        tarefa.ordem = request.form.get('ordem', type=int)
        tarefa.data_alteracao = datetime.utcnow()
        # Adicione ou atualize outros campos conforme necessário

        try:
            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar tarefa: {e}', 'error')

        return redirect(url_for('editar_tarefa', id=id))
    else:
        flash('Tarefa não encontrada.', 'error')
        return redirect(url_for('index'))  # Assumindo que você tem uma rota 'index'
