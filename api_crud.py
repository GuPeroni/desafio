import uvicorn, requests, json
from app import app
from db import Banco


# Faz a inserção dos dados no banco com as validações que caso já tenha o cpf ele não add novamente e com outras validações também

@app.post('/inserir_dados/{nome}/{dta_nascimento}/{cpf}/{cep}/{token_autenticacao}')
def inserir(nome: str, dta_nascimento: str, cpf: str, cep: str, token_autenticacao: str):

    """
    INSERE OS DADOS NO BANCO

    """

    db = Banco()

    query = 'SELECT * FROM tokens'

    ret = db.retorna_consulta(query)

    for rets in ret:
        if token_autenticacao == rets[0]:

            if len(cep) == 8:

                url = "https://viacep.com.br/ws/{}/json/".format(cep)

                response = requests.request("GET", url)

                converter_json = json.loads(response.text)

                try:

                    rua = converter_json['logradouro']
                    bairro = converter_json['bairro']
                    cidade = converter_json['localidade']
                    estado = converter_json['uf']

                except:
                    return {'Status': 404, 'Mensagem': 'CEP Inválido'}
            else:
                return {'Status': 404, 'Mensagem': 'Números de digitos inválidos'}
            
            if len(cpf) == 11:

                query = "SELECT * FROM clientes where cpf = '{}'".format(cpf)
                retorna_todos = db.retorna_consulta(query)

                if retorna_todos:
                    return {'Status': 404, 'Mensagem': 'Cpf já inserido'}
                else:
                    query = "INSERT INTO clientes(nome, data_nascimento, cpf, cep, rua, bairro, cidade, estado) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(nome, dta_nascimento, cpf, cep, rua, bairro, cidade, estado)
                    db.executa_comando(query)

                    return {'Status': 200, 'Mensagem': 'Dados Gravados com sucesso'}
            else:
                return {'Status': 404, 'Mensagem': 'Cpf Inválido'}

    else:
        return {'Status': 400, 'Mensagem': 'Falha na autenticação'}


# Pegas todas as informações do banco

@app.get('/listar_todos/{token_autenticacao}')
def get_all(token_autenticacao: str):

    """
    RETORNA TODOS OS DADOS DO BANCO

    """

    db = Banco()

    query = 'SELECT * FROM tokens'

    ret = db.retorna_consulta(query)

    for rets in ret:
        if token_autenticacao == rets[0]:

            query = 'SELECT * from clientes'
            retorna_todos = db.retorna_consulta(query)

            return retorna_todos
        else:
            return {'Status': 400, 'Mensagem': 'Falha na autenticação'}

# Traz as informações de acordo com o nome do usuario que tem no banco

@app.get('/listar_usr/{nome_usuario}/{token_autenticacao}')
def usuario_especifico(nome_usuario: str, token_autenticacao: str):

    """
    RETORNA UM USUARIO ESPECIFICO DO BANCO

    """

    db = Banco()

    query = 'SELECT * FROM tokens'

    ret = db.retorna_consulta(query)

    for rets in ret:
        if token_autenticacao == rets[0]:

            if nome_usuario:
                query = "SELECT * FROM clientes where nome = '{}'".format(nome_usuario)

                retorna_dados = db.retorna_consulta(query)

                if not retorna_dados:
                    return {'Status': 404, 'Mensagem': 'Usuario não encontrado'}

                return retorna_dados
        else:
            return {'Status': 400, 'Mensagem': 'Falha na autenticação'}

# Deleta um dado pelo id             

@app.post('/deletar_usr/{id}/{token_autenticacao}')
def delete_user(id: str, token_autenticacao: str):

    """
    DELETA UM USUARIO DO BANCO

    """

    db = Banco()

    query = 'SELECT * FROM tokens'

    ret = db.retorna_consulta(query)

    for rets in ret:
        if token_autenticacao == rets[0]:    

            if id:
                query = "DELETE FROM clientes where id_cliente = {}".format(id)
                executa = db.executa_comando(query)
                return {'Status': 200, 'Mensagem': 'Usuario deletado com sucesso'}

            else:
                return {'Status': 404, 'Mensagem': 'Usuario não encontrado'}
        else:
            return {'Status': 400, 'Mensagem': 'Falha na autenticação'}

# Atualiza os dados de acordo com o campo e o valor do campo que você passar            

@app.put('/atualizar/{campo}/{valor_campo}/{id}/{token_autenticacao}')
def atualizar_dados(campo: str, valor_campo: str, id: str, token_autenticacao: str):

    """
    FAZ UPDATE DOS DADOS NO BANCO

    """

    db = Banco()

    query = 'SELECT * FROM tokens'

    ret = db.retorna_consulta(query)

    for rets in ret:
        if token_autenticacao == rets[0]:        

            if id:
                query = "UPDATE clientes SET {} = '{}' WHERE id_cliente = {}".format(campo, valor_campo, id)
                db.executa_comando(query)

                return {'Status': 200, 'Mensagem': 'Update realizado com sucesso'}

            else:
                return {'Status': 404, 'Mensagem': 'Usuario não encontrado'}
        else:
            return {'Status': 400, 'Mensagem': 'Falha na autenticação'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)