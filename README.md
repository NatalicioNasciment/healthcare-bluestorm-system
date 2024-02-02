# Healthcare Bluestorm Api

___
Decisões Arquiteturais do Projeto
---
Escolhi o flask para esse projeto pelo nivel de abstração que ele proporciona, permitindo facilmente trocar alguma extensão. E pela fato de ser um microframework apresenta um alto nivel de desempenho.

Seguí um modelo arquitetural voltado para a camada de negócio. Apesar da aplicação utilizar alguns plugins de terceiros(que ficam no modulo ext), no geral o projeto em si é agnostico em relação a uma extensão específica.

Utilizei o padrão aplication factory que encapsula o app em um método, faz alguma alteração e o retorna modifcado, para não existir a possibilidade de importar o app diretamente e acabar gerando o famoso circular import.



## Clone

```bash
git clone https://github.com/NatalicioNasciment/healthcare-bluestorm-system.git
```

___
Versão do Python utilizada
---
Python 3.9+

## Instalação 



```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -r requirements_test.txt
```
Uitlizando Script:  
```bash
 make install
```
## Docker
```bash
# Criando a imagem apartir do Dockerfile  
1. docker build -t  healthcare-bluestorm-api .
2. docker run --name healthcare-bluestorm-api -d -p 5000:5000 healthcare-bluestorm-api
```
ou
```bash
# Baixando  a imagem diretamente do dockerhub  
1. docker pull natalicionascimento/healthcare-bluestorm-api
2. docker run --name healthcare-bluestorm-api -d -p 5000:5000 healthcare-bluestorm-api
```




## Endpoints Disponiveis:

___
• auth (Rota para obter o token de acesso para as demais rotas)
---
```bash
curl --location --request POST 'localhost:5000/api/v1/auth' \
--header 'username: teste' \
--header 'password: teste'

#Essa requisição retornar algo do tipo:
{"expire":"Fri, 02 Feb 2024 02:09:19 GMT","id":"USER1","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlVTRVIxIiwiZXhwaXJlIjoxNzA2ODM5NzU5LjEyMjM2OH0.cp_WD7k1AlotgVRrjwprtBiby7OGVmZuzfcYrrq5PcE"}
````


___
• patients (listagem de pacientes, também foi implementado query_string e é possivel filtrar por campos especificos)
---
```bash
curl --location 'localhost:5000/api/v1/patients?first_name=JOA' \
--header 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlVTRVIxIiwiZXhwaXJlIjoxNzA2ODA5OTg0Ljg0Nzg3Nn0.6bgUbYfXkgUwruFhJxTfSk1t9veIiV-3Eg4Lihg8MyI' \
--header 'uuid: USER1'

#Essa requisição retornar algo do tipo:
[
    {
        "date_of_birth": "1996-10-25T00:00:00",
        "first_name": "JOANA",
        "last_name": "SILVA",
        "uuid": "PATIENT0001"
    },
    {
        "date_of_birth": "1980-07-23T00:00:00",
        "first_name": "JOANA",
        "last_name": "FERREIRA",
        "uuid": "PATIENT0035"
    }
]
````

___
• pharmacies (listagem de farmacias, também foi implementado query_string e é possivel filtrar por campos especificos)
---
```bash
curl --location 'localhost:5000/api/v1/pharmacies?name=DROGA%20MAIS' \
--header 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlVTRVIxIiwiZXhwaXJlIjoxNzA2ODM5OTk2LjkyMjEyM30.YRc3BfcZv7Eq3SgH1kxtbgfBi3arheY739Il8FtIFm4' \
--header 'uuid: USER1'

#Essa requisição retornar algo do tipo:

[
    {
        "city": "RIBEIRAO PRETO",
        "name": "DROGA MAIS",
        "uuid": "PHARM0001"
    },
    {
        "city": "SAO PAULO",
        "name": "DROGA MAIS",
        "uuid": "PHARM0006"
    }
]

````

___
• transactions (listagem de transações, também foi implementado query_string e é possivel filtrar por campos especificos)
---
---
```bash
curl --location 'localhost:5000/api/v1/transactions?uuid=TRAN0001' \
--header 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlVTRVIxIiwiZXhwaXJlIjoxNzA2ODQwMzMwLjUxNTQ3OH0.Pflk71wzEDU_9kmUyEXFVTeHDRm8ZHMEJJMBHy4FWI8' \
--header 'uuid: USER1'

#Essa requisição retornar algo do tipo:

[
    {
        "amount": "3.50",
        "patient": {
            "date_of_birth": "1993-09-30T00:00:00",
            "first_name": "CRISTIANO",
            "last_name": "SALOMAO",
            "uuid": "PATIENT0045"
        },
        "pharmacy": {
            "city": "CAMPINAS",
            "name": "DROGAO SUPER",
            "uuid": "PHARM0008"
        },
        "timestamp": "2020-02-05 07:49:03.000000",
        "uuid": "TRAN0001"
    }
]

````

## Estrutura do Projeto

```bash
.
├── Makefile
├── healthcare_bluestorm_system  (MAIN PACKAGE)
│   ├── app.py  (APP FACTORIES)
│   ├── blueprints  (BLUEPRINT FACTORIES)
│   │   ├── __init__.py
│   │   ├── restapi  (REST API)
│   │   │   ├── __init__.py
│   │   │   └── resources.py
│   │   └── webui  (FRONT END)
│   │       ├── __init__.py
│   ├── ext (EXTENSION FACTORIES)
│   │   ├── admin.py
│   │   ├── appearance.py
│   │   ├── auth.py
|   |   |__authentication.py
│   │   ├── commands.py
│   │   ├── configuration.py
│   │   ├── database.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models.py  (DATABASE MODELS)
│   └── tests  (TESTS)
│       ├── conftest.py
│       ├── __init__.py
│       └── test_user_authentication.py
├── README.md
├── requirements_dev.txt
├── requirements_test.txt
├── requirements.txt
└── settings.toml  (SETTINGS)
