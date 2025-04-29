# Sistema-Banc-rio-Distribu-do
 Projeto: Sistema de Gerenciamento de Contas Bancárias com gRPC, Python e Redis
Trabalho da disciplina Sistemas Distribuídos: desenvolvimento de um sistema distribuído para gerenciar contas bancárias, utilizando:

gRPC para comunicação cliente-servidor,

Python como linguagem principal,

Redis como banco de dados em memória,

Suporte a concorrência para múltiplos clientes simultâneos.

Tecnologias Utilizadas
Python 3.10+

gRPC (grpcio, grpcio-tools)

Redis

Biblioteca redis-py

Multithreading (concurrent.futures)

/Sistemas_Distribuidos
│
├── bank.proto                 # Definição dos serviços e mensagens gRPC
├── bank_pb2.py                 # Código gerado automaticamente do proto
├── bank_pb2_grpc.py            # Código gerado automaticamente do proto (gRPC)
│
├── server.py                   # Servidor gRPC que conecta ao Redis
├── client.py                   # Cliente gRPC para operações básicas
├── simulate_clients.py         # Script para testar concorrência
├── client_test_errors.py       # Script para testar erros obrigatórios
│
└── README.md                   # Documentação do projeto



Como Executar o Projeto

é melhor usar um ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install grpcio grpcio-tools redis


rodar o redis:
docker run -d -p 6379:6379 --name redis redis


Gerar os arquivos .py do .proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bank.proto

Rodar o Servidor
python3 server.py

Rodar o Cliente
python3 client.py

Rodar Simulação de Concorrência (20 clientes simultâneos)
python3 simulate_clients.py

Rodar Testes de Erro
python3 client_test_errors.py

