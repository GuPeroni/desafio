from fastapi.testclient import TestClient
from api_crud import app
import pytest 

#Executar pelo terminal esse comando para fazer os testes -> pytest testes_unitarios.py 

teste = TestClient(app)


def test_get():
    response = teste.get('/listar_todos/09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    assert response.status_code == 200

def test_token():
    response = teste.get('/listar_usr/Gustavo/1255854588785454585445')
    assert response.status_code == 200
    assert response.json() == {"Status":400,"Mensagem":"Falha na autenticação"}

def test_post():
    response = teste.post('/inserir_dados/Carlos/25-10-2010/44756996352/09781220/09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    assert response.status_code == 200
    assert response.json() == {"Status":200,"Mensagem":"Dados Gravados com sucesso"}

def test_atualizao():
    response = teste.put('/atualizar/nome/Pedro/3/09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    assert response.status_code == 200
    assert response.json() == {"Status":200,"Mensagem":"Update realizado com sucesso"}


