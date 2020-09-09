# Emprestapi

### API para gerenciamento de empréstimos (Desafio Onidata)

## Configuração
* É necessário clonar o repositório com o comando

```
$ git clone https://github.com/IagoCarvalho/api-emprestimos.git
```

* Para subir a aplicação utilize o comando
```
$ docker-compose up
```

* **Caso não seja possível conectar a database ou ocorra algum problema na criação do container**
```
$ docker-compose up --build --force-recreate --no-dep
```

* Determine o id do container web com

```
$ sudo docker ps
```

* Faça as migrações com
```
$ sudo docker exec -it CONTAINER-ID python manage.py makemigrations
$ sudo docker exec -it CONTAINER-ID python manage.py migrate
```

* Para executar os testes
```
$ sudo docker exec -it CONTAINER-ID python manage.py test
```

## Endpoints

### Usuários
```
POST /users/rest_auth/registration/
PARAMS username, email, password1, password2
```

**Endpoint desprotegido para fim auxiliar de listagem**
```
GET /users/list
```

```
POST /users/rest_auth/login/
PARAMS username, password, email
```


### Empréstimos
```
POST /financials/loans/new
PARAMS nominal_value, interest_rate, bank, acquittance_time
HEADERS Authorization Token
```

```
GET /financials/loans/list
HEADERS Authorization Token
```

```
GET /financials/loans/<int:id>/detail
HEADERS Authorization Token
```

### Pagamentos
```
POST /financials/payment/create
PARAMS value, loan
HEADERS Authorization Token
```

```
GET /financials/payments
HEADERS Authorization Token
```

```
GET /financials/payments/<int:id>
HEADERS Authorization Token
```