# Backend Python - Clinica Veterinaria (integracao com MySQL)

Integracao do script `clinica_veterinaria_2a_entrega_lab.sql` com Python usando
`mysql-connector-python`. O codigo e separado em **Models** e **DAOs** (um
arquivo por tabela) e oferece um **menu interativo** no terminal para fazer
Insert, Update, Delete e Select em cada tabela.

## Estrutura de pastas

```
backend/
├── config.py            # dados de conexao com o MySQL
├── database.py          # DatabaseManager (conexao + helpers de query)
├── main.py              # menu interativo (orientado a dados)
├── requirements.txt
├── models/              # uma dataclass por tabela
│   ├── dono.py  veterinario.py  animal.py
│   └── prontuario.py  servico.py  consulta.py
└── dao/                 # uma classe CRUD por tabela
    ├── base_dao.py      # Insert/Find/Update/Delete genericos
    ├── dono_dao.py  veterinario_dao.py  animal_dao.py
    └── prontuario_dao.py  servico_dao.py  consulta_dao.py
```

O `BaseDAO` concentra o CRUD compartilhado; cada DAO concreto so declara seu
`table/pk/model` e adiciona suas proprias buscas e queries com JOIN, evitando
codigo duplicado.

## Como executar

1. Rode o `clinica_veterinaria_2a_entrega_lab.sql` (raiz do repositorio) no MySQL Workbench.
2. Ajuste usuario/senha no `config.py`.
3. `pip install -r requirements.txt`
4. `cd backend && python main.py`

## Requisitos atendidos

- Models e DAOs em pastas separadas (nada feito direto na `main`).
- CRUD completo (Insert/Update/Delete/Select) para as 6 tabelas pelo menu.
- Busca por atributo em cada entidade (nome, especialidade, especie, id do
  animal, nome e data).
- Mais de 3 SELECTs com JOIN (opcao 7 nos menus de Animais / Prontuarios /
  Servicos / Consultas): animal+dono, prontuario+animal, servico+veterinario e
  consulta+animal+dono+veterinario.
- O script `.sql` termina com `SELECT * FROM` de cada tabela, para acompanhar
  as mudancas feitas pelo backend acontecendo ao vivo no banco.
