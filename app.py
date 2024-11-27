from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Simulação de banco de dados
db = {
    "usuarios": [],
    "eventos": [],
    "inscricoes": []
}

# Rota principal: Login
@app.route('/')
def index():
    return render_template('login.html')

# Cadastro de usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Coleta dados do formulário
        novo_usuario = {
            "nome": request.form['nome'],
            "email": request.form['email'],
            "senha": request.form['senha']
        }
        # Adiciona ao banco de dados simulado
        db['usuarios'].append(novo_usuario)
        return redirect(url_for('index'))
    return render_template('cadastro.html')

# Gerenciamento de eventos (criação, edição, exclusão)
@app.route('/eventos', methods=['GET', 'POST'])
def eventos():
    if request.method == 'POST':
        # Coleta dados do formulário
        novo_evento = {
            "id": len(db['eventos']) + 1,
            "titulo": request.form['titulo'],
            "descricao": request.form['descricao'],
            "data": request.form['data']
        }
        # Adiciona evento ao banco de dados
        db['eventos'].append(novo_evento)
        return redirect(url_for('eventos'))
    return render_template('eventos.html', eventos=db['eventos'])

@app.route('/eventos/editar/<int:evento_id>', methods=['GET', 'POST'])
def editar_evento(evento_id):
    evento = next((e for e in db['eventos'] if e['id'] == evento_id), None)
    if not evento:
        return "Evento não encontrado.", 404
    if request.method == 'POST':
        evento['titulo'] = request.form['titulo']
        evento['descricao'] = request.form['descricao']
        evento['data'] = request.form['data']
        return redirect(url_for('eventos'))
    return render_template('eventos.html', evento=evento)

@app.route('/eventos/excluir/<int:evento_id>', methods=['POST'])
def excluir_evento(evento_id):
    db['eventos'] = [e for e in db['eventos'] if e['id'] != evento_id]
    return redirect(url_for('eventos'))

# Inscrição e cancelamento
@app.route('/inscricoes', methods=['GET', 'POST'])
def inscricoes():
    if request.method == 'POST':
        evento_id = int(request.form['evento_id'])
        usuario_email = request.form['email']
        # Adiciona a inscrição
        db['inscricoes'].append({"evento_id": evento_id, "email": usuario_email})
        return redirect(url_for('inscricoes'))
    return render_template('inscricoes.html', eventos=db['eventos'], inscricoes=db['inscricoes'])

@app.route('/inscricoes/cancelar/<int:evento_id>', methods=['POST'])
def cancelar_inscricao(evento_id):
    db['inscricoes'] = [i for i in db['inscricoes'] if i['evento_id'] != evento_id]
    return redirect(url_for('inscricoes'))

# Visualização de eventos
@app.route('/visualizacao')
def visualizacao():
    return render_template('visualizacao.html', eventos=db['eventos'])

# Retorna o banco de dados simulado para debug (opcional)
@app.route('/db')
def debug_db():
    return jsonify(db)

if __name__ == '__main__':
    app.run(debug=True)
