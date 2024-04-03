from datetime import datetime

def create_db(app,db):
    class Tarefa(db.Model):
        __tablename__ = "tarefas"
        id = db.Column(db.Integer, primary_key=True)
        descricao = db.Column(db.String(200))
        feita = db.Column(db.Boolean)
        data_primeira_vez = db.Column(db.DateTime)
        data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
        data_alteracao = db.Column(db.DateTime, onupdate=datetime.utcnow)
        intervalo_repeticao_mode = db.Column(db.String(50))
        intervalo_repeticao_value = db.Column(db.String(50))
        proximo_domingo = db.Column(db.Boolean)
        data_proxima = db.Column(db.DateTime)
        data_proxima_seguinte = db.Column(db.DateTime)
        classe = db.Column(db.Integer)
        notas = db.Column(db.String(200))
        ordem = db.Column(db.Integer)
        owner = db.Column(db.String(50))
        

    with app.app_context():
        db.create_all()  # Criação das tabelas
        db.session.commit()  # Execução das tarefas pendentes da base de dados

    return Tarefa
