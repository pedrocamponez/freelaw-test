# Planejamento e Design de Arquitetura

## Requisitos Funcionais:

#### CRUD de usuários;
#### CRUD de eventos;
#### Inscrição de participantes;
#### Notificações;
#### Processamento assíncrono;
#### Relatórios;

## Requisitos Não Funcionais:

#### Escalabilidade;
#### Performance;
#### Segurança;
#### Testes;
#### Documentação;

## Arquitetura:

#### Monolito - Model, Serializer, View
#### Backend: Django + Django REST Framework
#### Processamento Assíncrono: Redis, Celery
#### Banco de Dados: PostgreSQL
#### Autenticação: JWT (SimpleJWT)
#### Serviço de Email: SendGrid
#### Deploy: Docker, Kubernetes, CI/CD
#### Documentação: Swagger

# Executando a aplicação localmente:
### Clone este repositório:
#### git clone https://github.com/pedrocamponez/freelaw-test/

### Acesse o arquivo no qual clonou o repositório, crie um ambiente virtual na linha de comando e ative-o
#### [WINDOWS] > py -m venv _env
#### [WINDOWS] > .\_env\Scripts\activate

#### [MAC]     > python3 -m venv _env
#### [MAC]     > source _env/bin/activate

### Após ativar, instale o requirements.txt
#### pip install -r requirements.txt

### Após todas as dependências instaladas, faça as migrações do banco de dados:
#### python manage.py makemigrations
#### python manage.py migrate

### Agora, execute o servidor
#### python manage.py runserver

### É necessário que o Redis esteja rodando em sua máquina para que o Celery funcione. Caso não tenha o Redis (Linux/Mac) ou esteja em um Windows, você pode usar o Docker para rodar o Redis.
#### Com o Docker Desktop rodando, ou o Docker funcionando em sua máquina (Linux/Mac), digite o seguinte código em seu terminal:
#### docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

### Agora, execute o comando para iniciar o Celery:
#### Na raiz do projeto, digite: celery -A freelawtest worker --pool=solo -l info (Utilizei esse comando em vez do worker padrão porque estava bugando no Windows).

## Com todas as aplicações rodando, acesse http://localhost:8000/api/docs para ver a documentação Swagger completa da API

## Qualquer dúvida, entre em contato através do email camponezpedro@gmail.com ou https://www.linkedin.com/in/pedrocamponez

## Obrigado
