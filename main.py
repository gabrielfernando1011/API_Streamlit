# SQL_ALCHEMY
# pip install pymysql 
# Permite a conexao da API com o banco de dados
# pip install flask_sqlalchemy
# Flask - permite a criacao de API com Python
# Response e Request -> Requisicao
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('carros')

# Rastrear as modificacoes realizadas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Configuracao de conexao com o banco
# %40 -> faz o papel do @
# 1 - Usuario (root) 2 - Senha (Senai%40134) 3 - localhost (127.0.0.1) 4 - nome do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40134@127.0.0.1/db_carro'

mybd = SQLAlchemy(app)

# Classe para definir o modelo dos dados que correspondem a tabela do banco de dados
class Carros(mybd.Model):
    __tablename__ = 'tb_carro'
    id_carro = mybd.Column(mybd.Integer, primary_key=True)
    marca = mybd.Column(mybd.String(255))
    modelo = mybd.Column(mybd.String(255)) 
    ano = mybd.Column(mybd.String(255)) 
    cor = mybd.Column(mybd.String(255))
    valor = mybd.Column(mybd.String(255))
    numero_Vendas = mybd.Column(mybd.String(255))

# Esse metodo to_json vai ser usado para converter o objeto em json
    def to_json(self):
        return {
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "valor": float(self.valor),
            "cor":self.cor,
            "numero_Vendas": self.numero_Vendas
        }

# ---------------------------------------------------
#METODO 1 - GET
@app.route('/carros', methods=['GET'])
def seleciona_carro():
    carro_selecionado = Carros.query.all()
    # Executa uma consulta no banco de dados (SELECT * FROM tb_carro)
    carro_json = [carro.to_json()
                  for carro in carro_selecionado]
    return gera_resposta(200, "carros", carro_json)


# -----------------------
# METODO 2 - GET (POR ID)
@app.route('/carros/<id_carro_pam>', methods=['GET'])
def seleciona_carro_id(id_carro_pam):
    carro_selecionado = Carros.query.filter_by(id_carro=id_carro_pam).first()
    # SELECT * FROM tb_carro WHERE id_carro = 5
    carro_json = carro_selecionado.to_json()

    return gera_resposta(200, "carros", carro_json, 'Carro encontrado!')


# -------------------
# METODO 3 - POST - ACRESCENTA UMA TABELA NOVA - ID NOVO
@app.route('/carros', methods=['POST'])
def criar_carro():
    requisicao = request.get_json()

    try:
        carro = Carros(
             id_carro = requisicao['id_carro'],
            marca = requisicao['marca'], 
            modelo = requisicao['modelo'], 
            ano = requisicao['ano'], 
            cor = requisicao['cor'], 
            valor = requisicao['valor'], 
            numero_Vendas = requisicao['numero_Vendas']
        )

        # Adiciona ao banco
        mybd.session.add(carro)
        # Salva
        mybd.session.commit()

        return gera_resposta(201, "carro", carro.to_json(), "Criado com Sucesso!")

    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao Cadastrar!")
    

# --------------
# METODO 4 - DELETE
@app.route('/carros/<id_carro_pam>', methods=['DELETE'])
def deleta_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()

    try:
        mybd.session.delete(carro)
        mybd.session.commit()
        return gera_resposta(200, "carro", carro.to_json(), "Deletado com Sucesso!")
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "carro",{}, "Erro ao Deletar!")



# ------------
# METODO 5 - (PUT)
@app.route('/carros/<id_carro_pam>', methods=['PUT'])
def atualiza_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()
    requisicao = request.get_json()

    try:
        if('marca' in requisicao):
            carro.marca = requisicao['marca']
        if ('modelo' in requisicao):
            carro.modelo = requisicao['modelo']
        if('ano' in requisicao):
            carro.ano = requisicao['ano']
        if ('cor' in requisicao):
            carro.cor = requisicao['cor']
        if('valor' in requisicao):
            carro.valor = requisicao['valor']
        if ('numero_Vendas' in requisicao):
            carro.numero_Vendas = requisicao['numero_Vendas']
        
        mybd.session.add(carro)
        mybd.session.commit()

        return gera_resposta(200, "carro", carro.to_json(), "Carro Atualizado com Sucesso!")
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "carro",{}, "Erro ao Atualizar!")




# ------------
# RESPOSTA PADRAO
    # - status (200,201)
    # - nome do conteudo
    # - conteudo
    # - mensagem(opcional)
def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem
    
    return Response(json.dumps(body), status=status, mimetype='application/json')
# Dumps - Converte o discionario criado (body) em json (json.dumps)


app.run(port=5000, host='localhost', debug=True)
