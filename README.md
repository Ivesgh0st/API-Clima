# API de Clima e Cidades

API desenvolvida como projeto acadêmico para a disciplina de Desenvolvimento de Sistemas. Recebe o nome de uma cidade e retorna informações climáticas em tempo real, além de listar municípios por estado.

## Equipe

| Nome | Matrícula |
|------|-----------|
| Ives Carneiro Sebestyen | 2412834 |
| José Teofilo Silva Junior | 2326318 |
| Eric Vinicius Dias Aquino | 2326242 |
| Gabriel Eduardo Brasil | 2124682 |
| Desireh Mharinnes Anna Gomes De Araujo | 2323808 |
| Matheus Correia Azevedo | 2425053 |

## Como rodar

**1. Instale as dependências:**
```bash
python -m pip install -r requirements.txt
```

**2. Inicie a API:**
```bash
python src/main.py
```

A API vai estar disponível em `http://localhost:3000`. Acesse `http://localhost:3000/docs` para ver e testar todos os endpoints pelo navegador.

**3. Rode os testes:**
```bash
python -m pytest tests/test_api.py -v
```

## Endpoints

### GET /api/v1/clima/{nome_cidade}
Retorna o clima atual de uma cidade.

```bash
curl http://localhost:3000/api/v1/clima/Fortaleza
```

```json
{
  "nome": "Fortaleza",
  "estado": "CE",
  "clima": {
    "temperatura_min": 24,
    "temperatura_max": 32,
    "condicao": "Parcialmente Nublado"
  }
}
```

---

### GET /api/v1/cidades/{sigla_uf}
Lista os municípios de um estado.

```bash
curl http://localhost:3000/api/v1/cidades/CE
```

```json
{
  "uf": "CE",
  "quantidade_retornada": 10,
  "cidades": [
    { "nome": "Fortaleza" },
    { "nome": "Caucaia" }
  ]
}
```

---

### GET /api/v1/health
Verifica se a API e os serviços externos estão funcionando.

```bash
curl http://localhost:3000/api/v1/health
```

```json
{
  "status": "healthy"
}
```

## Tecnologias

- **Python 3.8+**
- **FastAPI** — framework da API
- **httpx** — requisições HTTP assíncronas
- **pytest** — testes automatizados
- **Open-Meteo** — coordenadas e dados climáticos
- **Brasil API (IBGE)** — lista de municípios

## Observação

As coordenadas das cidades são buscadas dinamicamente pelo nome — nenhuma coordenada está fixada no código.

## Testando no Postman

Importe o arquivo `docs/postman_collection.json` no Postman para ter todos os endpoints prontos para teste.
