# edit -> nome_pasta + caminho_pasta

# source venv/bin/activate
# pip install flask (feito)
# pip install Flask-SQLAlchemy (feito)
# pip install sqlalchemy
# python app.py

from app_files.adiar import adiar
from app_files.BDcriar import create_db
from app_files.criar import criar
from app_files.editar import editar
from app_files.eliminar import eliminar
from app_files.feita import feita
from app_files.filtro import exibirFiltroCustom
from app_files.importCSV import criar_tarefas
from app_files.refresh import refresh
from datetime import datetime

from flask import render_template, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


app = Flask(__name__)
app.secret_key = 'chave'

nome_pasta_projeto = 'projeto tarefas oficial'
caminho_ate_projeto = 'https://github.com/StephaniePlatvoet/app-tarefas-free.git'
nome_pasta_database = '/database'
caminho_pasta_database = caminho_ate_projeto + nome_pasta_database


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + caminho_pasta_database + '/tarefas.db'
db = SQLAlchemy(app)
app.config["DEBUG"] = True

Tarefa = create_db(app,db)

@app.route('/')
def go_home():
    return exibirFiltroCustom(Tarefa, db)

# refresh

@app.route('/refresh')
def call_refresh():
    return refresh(Tarefa,db)

@app.route('/refresh0')
def call_refresh0():
    return refresh(Tarefa,db,classe_filter=0)


# filtros date
@app.route('/exibir_filtro_steph_min', methods=['GET'])
def exibirFiltroStephmin():
    return exibirFiltroCustom(Tarefa, db, owner='steph', filtrar_data_mais_proxima=True)


@app.route('/exibir_filtro_steph', methods=['GET'])
def exibirFiltroSteph():
    return exibirFiltroCustom(Tarefa, db, owner='steph')

@app.route('/exibir_filtro', methods=['GET'])
def do_filter():
    return exibirFiltroCustom(Tarefa, db, owner=None, filtrar_data_mais_proxima=True)


@app.route('/exibir_todas', methods=['GET'])
def exibir_todas():
    return exibirFiltroCustom(Tarefa, db)

# edit tarefa
@app.route('/tarefa-feita/<id>')
def tarefa_feita(id):
    return feita(Tarefa,db,id)

@app.route('/tarefa-adiar/<id>')
def tarefa_adiar(id):
    return adiar(Tarefa,db,id)


@app.route('/atualizar_tarefa/<int:id>', methods=['POST'])
def atualizar_tarefa(id):
    return editar(Tarefa,db,id)


@app.route('/editar_tarefa/<int:id>', methods=['GET'])
def editar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    return render_template('editar_tarefa.html', tarefa=tarefa)

# calendario
@app.route('/calendario', methods=['GET'])
def calendario():
    # Número total de tarefas a mostrar no calendário
    total_tarefas = 35
    hoje = datetime.utcnow().date()

    # Query das tarefas ordenadas por data_proxima
    tarefas_query = Tarefa.query.filter(or_(Tarefa.owner == 'steph', Tarefa.owner == 'ambos'),Tarefa.classe == 0).order_by(Tarefa.data_proxima.asc()).limit(total_tarefas).all()

    # Inicializar estrutura dos dias da semana
    dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    calendario_semanal = {dia: [] for dia in dias_da_semana}

    # Distribuir tarefas pelos dias da semana
    for i, tarefa in enumerate(tarefas_query):
        dia_index = i % 7  # Isso garante a distribuição uniforme
        dia_nome = dias_da_semana[dia_index]
        calendario_semanal[dia_nome].append(tarefa)

    # Passa o calendário_semanal para o template
    return render_template('calendario.html', calendario_semanal=calendario_semanal, datetime=datetime)

# eliminar tarefa

@app.route('/eliminar-tarefa/<id>')
def eliminar_tarefa(id):
    return eliminar(Tarefa,db,id)


# criar tarefas
    
@app.route('/criar-tarefa', methods=['POST'])
def criar_tarefa():
    return criar(Tarefa,db)

@app.cli.command("import-csv-birthdays") #flask import-csv-birthdays
def import_csv():
    name_csv_file = caminho_pasta + '/Livro6.csv'
    criar_tarefas(Tarefa, db,name_csv_file)

@app.cli.command("import-csv") #flask import-csv
def import_csv():
    name_csv_file = caminho_pasta + '/Livro4.csv'
    criar_tarefas(Tarefa, db,name_csv_file)

if __name__ == "__main__":
    app.run(debug=True)

#flask import-csv
#flask import-csv-birthdays
# app_files app.py
# conda deactivate
# ngrok http 127.0.0.1:5000
# sqlite3 database/tarefas.db (SQLite version 3.39.5 ) ; .databases ; .tables ; .exit ; select * from tarefas ; SELECT name FROM pragma_table_info('tarefas') ;


# app_files --version (Python 3.9.6);
# pip --version (pip 22.3.1);
# ngrok --version (ngrok version 3.3.1);
# brew --version (Homebrew 4.1.0);
# flask-ngrok (6.8.0) ;
# wget --version (GNU Wget 1.21.4 compilado a darwin22.4.0
