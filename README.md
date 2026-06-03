# Weather API

**API de Informações de Cidades e Clima**

Uma API RESTful moderna desenvolvida com FastAPI que fornece informações detalhadas sobre clima e cidades brasileiras. A aplicação busca coordenadas dinamicamente através do nome da cidade e integra-se com serviços externos confiáveis para fornecer dados precisos e atualizados.

<<<<<<< HEAD
---

## 👥 Integrantes da Equipe

| Nome Completo | Matrícula | Papel |
|---|---|---|
| José teofilo Silva Junior | 2326318 | Desenvolvedor Backend |
| Eric Vinicius Dias Aquino | 2326242 | Desenvolvedor Backend |
| Gabriel Eduardo Brasil | 2124682 | Desenvolvedor Backend |
| Desireh Mharinnes Anna Gomes De Araujo | 2323808 | Desenvolvedor Backend |
| Matheus Correia Azevedo | 2425053 | Desenvolvedor Backend |
| Ives Carneiro Sebestyen | 2412834 | Desenvolvedor Backend |

---

## 📋 Características

- **Busca Dinâmica de Coordenadas**: Localiza automaticamente as coordenadas de qualquer cidade brasileira pelo nome, integrando Brasil API e Open-Meteo.
- **Informações de Clima em Tempo Real**: Retorna temperatura mínima/máxima, condição climática e unidades de medida.
- **Listagem de Cidades por Estado**: Consulte todas as cidades de um estado específico com paginação (limite).
- **Verificação de Saúde**: Monitore o status da API e dos serviços externos integrados.
- **CORS Habilitado**: Permitindo integração simplificada com aplicações web via navegador.
- **Documentação Interativa**: Acesse a documentação Swagger em `/docs`.
- **Testes Automatizados**: Suíte de testes unitários validando cenários de sucesso e erro de acordo com as especificações.

---
=======
## 📋 Características

- **Busca Dinâmica de Coordenadas**: Localiza automaticamente as coordenadas de qualquer cidade brasileira pelo nome, sem usar valores fixos no código
- **Informações de Clima em Tempo Real**: Retorna temperatura mínima/máxima, condição climática e outros dados meteorológicos
- **Listagem de Cidades por Estado**: Consulte todas as cidades de um estado específico
- **Verificação de Saúde**: Monitore o status da API e dos serviços externos integrados
- **Documentação Interativa**: Acesse a documentação Swagger em `/docs`
- **Testes Automatizados**: Suite de testes incluindo cenários de sucesso e erro
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**
<<<<<<< HEAD
   ```bash
   git clone <seu-repositorio>
   cd weather-api
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a API**
   ```bash
   python src/main.py
   ```

A API estará disponível em `http://localhost:3000`

---

=======

```bash
git clone <seu-repositorio>
cd weather-api
```

2. **Instale as dependências**

```bash
pip install -r requirements.txt
```

3. **Execute a API**

```bash
python src/main.py
```

A API estará disponível em `http://localhost:3000`

>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
## 📚 Documentação da API

### Endpoints Disponíveis

#### 1. **GET /api/v1/health**

Verifica a saúde da API e dos serviços externos integrados.

**Exemplo de Requisição:**
```bash
curl http://localhost:3000/api/v1/health
```

<<<<<<< HEAD
**Resposta de Sucesso (200 - Saudável):**
```json
{
  "status": "healthy",
  "versao": "1.0.0",
  "timestamp": "2026-06-02T21:30:00Z"
}
```

**Resposta Degradada (200 - Serviço Externo Offline):**
```json
{
  "status": "degraded",
  "versao": "1.0.0",
  "timestamp": "2026-06-02T21:30:00Z",
  "motivo": "Serviço externo indisponível"
=======
**Resposta de Sucesso (200):**
```json
{
  "status": "healthy",
  "services": {
    "open_meteo": true,
    "brasil_api": true
  }
}
```

**Resposta Degradada (503):**
```json
{
  "status": "degraded",
  "services": {
    "open_meteo": false,
    "brasil_api": true
  }
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
}
```

---

#### 2. **GET /api/v1/clima/{nome_cidade}**

Retorna informações de clima de uma cidade específica.

**Parâmetros:**
<<<<<<< HEAD
- `nome_cidade` (string, obrigatório, na rota): Nome da cidade (pode ser parcial, mínimo de 2 caracteres)

**Exemplo de Requisição:**
```bash
curl http://localhost:3000/api/v1/clima/Fortaleza
=======
- `nome_cidade` (string, obrigatório): Nome da cidade (ex: "São Paulo", "Rio de Janeiro")

**Exemplo de Requisição:**
```bash
curl http://localhost:3000/api/v1/clima/São%20Paulo
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
```

**Resposta de Sucesso (200):**
```json
{
<<<<<<< HEAD
  "nome": "Fortaleza",
  "estado": "CE",
  "clima": {
    "temperatura_min": 24,
    "temperatura_max": 32,
    "condicao": "Parcialmente Nublado",
    "unidades": {
      "temperatura": "°C"
    }
  },
  "consultado_em": "2026-06-02T21:30:00Z"
}
```

**Resposta de Erro - Cidade Não Encontrada (404):**
```json
{
  "erro": true,
  "codigo": "CIDADE_NAO_ENCONTRADA",
  "mensagem": "Nenhuma cidade encontrada com o nome informado",
  "nome_informado": "CidadeInexistente"
}
```

**Resposta de Erro - Nome Inválido (400):**
```json
{
  "erro": true,
  "codigo": "NOME_INVALIDO",
  "mensagem": "O nome da cidade deve conter pelo menos 2 caracteres",
  "nome_informado": "X"
}
```

**Resposta de Erro - Serviço Externo Indisponível (503):**
```json
{
  "erro": true,
  "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
  "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
  "servico": "CPTEC"
=======
  "cidade": "São Paulo",
  "estado": "São Paulo",
  "temperatura_minima": 18.5,
  "temperatura_maxima": 28.3,
  "condicao_climatica": "Parcialmente nublado",
  "latitude": -23.5505,
  "longitude": -46.6333
}
```

**Resposta de Erro (404):**
```json
{
  "detail": "Cidade 'CidadeInexistente' não encontrada"
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
}
```

---

#### 3. **GET /api/v1/cidades/{sigla_uf}**

Lista todas as cidades de um estado específico.

**Parâmetros:**
<<<<<<< HEAD
- `sigla_uf` (string, obrigatório, na rota): Sigla do estado com exatamente 2 letras (ex: "CE", "SP")
- `limite` (integer, opcional, query parameter, default 10): Quantidade máxima de cidades a retornar (1-100)

**Exemplo de Requisição:**
```bash
curl "http://localhost:3000/api/v1/cidades/CE?limite=5"
=======
- `sigla_uf` (string, obrigatório): Sigla do estado com 2 caracteres (ex: "SP", "RJ", "MG")

**Exemplo de Requisição:**
```bash
curl http://localhost:3000/api/v1/cidades/SP
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
```

**Resposta de Sucesso (200):**
```json
{
<<<<<<< HEAD
  "uf": "CE",
  "quantidade_retornada": 5,
  "cidades": [
    { "nome": "Abaiara" },
    { "nome": "Acarape" },
    { "nome": "Acaraú" },
    { "nome": "Acopiara" },
    { "nome": "Aiuaba" }
  ],
  "consultado_em": "2026-06-02T21:30:00Z"
}
```

**Resposta de Erro - UF Não Encontrada (404):**
```json
{
  "erro": true,
  "codigo": "UF_NAO_ENCONTRADA",
  "mensagem": "Estado com a sigla informada não foi encontrado",
  "sigla_uf_informada": "XX"
}
```

**Resposta de Erro - Sigla UF Inválida (400):**
```json
{
  "erro": true,
  "codigo": "SIGLA_UF_INVALIDA",
  "mensagem": "A sigla do estado deve conter exatamente 2 letras",
  "sigla_uf_informada": "ceara"
=======
  "estado": "SP",
  "total_cidades": 645,
  "cidades": [
    {
      "id": 3509502,
      "name": "São Paulo"
    },
    {
      "id": 3509203,
      "name": "Campinas"
    },
    ...
  ]
}
```

**Resposta de Erro (400):**
```json
{
  "detail": "Sigla do estado deve ter 2 caracteres"
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
}
```

---

## 🧪 Testes

<<<<<<< HEAD
A API inclui testes automatizados para validar a funcionalidade e o tratamento de erros.
=======
A API inclui testes automatizados para validar funcionalidade e tratamento de erros.
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601

### Executar Testes

```bash
python -m pytest tests/test_api.py -v
```

### Cobertura de Testes

<<<<<<< HEAD
- Validação de sucesso para busca de clima em cidade válida.
- Tratamento de erro 404 para cidade não encontrada.
- Tratamento de erro 400 para nome de cidade muito curto.
- Validação de listagem de cidades com query parameter `limite`.
- Tratamento de erro 400 para sigla de estado inválida.
- Tratamento de erro 404 para estado (UF) inexistente.
- Validação do Health Check (saudável e degradado).

---

## 📮 Coleção Postman

Uma coleção completa do Postman está disponível em [postman_collection.json](file:///d:/Projetos%20David/ives/API-Clima--IVES/projeto_final/docs/postman_collection.json) para facilitar testes manuais dos endpoints.

---
=======
| Teste | Descrição | Status |
|-------|-----------|--------|
| `test_health_check_success` | Verifica se o endpoint de saúde retorna status correto | ✅ |
| `test_climate_success_sao_paulo` | Obtém clima de São Paulo com sucesso | ✅ |
| `test_climate_city_not_found` | Valida erro 404 para cidade inexistente | ✅ |
| `test_cities_success_sp` | Lista cidades de São Paulo com sucesso | ✅ |
| `test_cities_invalid_uf_format` | Valida erro 400 para sigla inválida | ✅ |
| `test_root_endpoint` | Testa endpoint raiz com informações da API | ✅ |

## 📮 Coleção Postman

Uma coleção completa do Postman está disponível em `docs/postman_collection.json` para facilitar testes manuais dos endpoints.

### Como Importar no Postman

1. Abra o Postman
2. Clique em "Import" (Importar)
3. Selecione o arquivo `docs/postman_collection.json`
4. A coleção será importada com todos os endpoints pré-configurados

## 🔧 Integração com Serviços Externos

### Open-Meteo API

Utilizada para:
- **Geocoding**: Buscar coordenadas de cidades pelo nome
- **Previsão de Clima**: Obter dados meteorológicos em tempo real

**Documentação:** https://open-meteo.com/

### Brasil API

Utilizada para:
- **Listagem de Cidades**: Obter lista completa de cidades por estado (IBGE)

**Documentação:** https://brasilapi.com.br/
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601

## 📁 Estrutura do Projeto

```
<<<<<<< HEAD
projeto_final/
├── src/
│   ├── __init__.py
│   └── main.py              # Código principal da API (FastAPI)
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Testes unitários automatizados (pytest)
├── docs/
│   └── postman_collection.json  # Coleção Postman exportada
├── requirements.txt         # Dependências do projeto
├── README.md               # Documentação principal
└── INTEGRANTES.md          # Identificação dos integrantes da equipe
```
=======
weather-api/
├── src/
│   ├── __init__.py
│   └── main.py              # Código principal da API
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Testes automatizados
├── docs/
│   └── postman_collection.json  # Coleção Postman
├── requirements.txt         # Dependências Python
├── README.md               # Este arquivo
└── INTEGRANTES.md          # Informações da equipe
```

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **FastAPI** | 0.104.1 | Framework web assíncrono |
| **Uvicorn** | 0.24.0 | Servidor ASGI |
| **httpx** | 0.25.2 | Cliente HTTP assíncrono |
| **pytest** | 7.4.3 | Framework de testes |
| **pytest-asyncio** | 0.21.1 | Suporte a testes assíncronos |

## 🌍 Variáveis de Ambiente

Atualmente, a API não requer variáveis de ambiente obrigatórias. Todos os endpoints externos são acessíveis publicamente.

## 📊 Exemplos de Uso

### Python

```python
import httpx
import asyncio

async def get_climate():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:3000/api/v1/clima/São Paulo")
        print(response.json())

asyncio.run(get_climate())
```

### JavaScript/Node.js

```javascript
fetch('http://localhost:3000/api/v1/clima/São Paulo')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erro:', error));
```

### cURL

```bash
# Obter clima
curl -X GET "http://localhost:3000/api/v1/clima/São%20Paulo"

# Listar cidades
curl -X GET "http://localhost:3000/api/v1/cidades/SP"

# Verificar saúde
curl -X GET "http://localhost:3000/api/v1/health"
```

## 🔐 Segurança

- A API não armazena dados sensíveis
- Todas as requisições aos serviços externos usam HTTPS
- Timeouts configurados para evitar requisições travadas
- Tratamento robusto de erros com mensagens informativas

## 📝 Notas Importantes

### Regra de Ouro: Coordenadas Dinâmicas

A aplicação **nunca** utiliza coordenadas fixas no código. Todas as coordenadas são buscadas dinamicamente através do nome da cidade usando a Open-Meteo Geocoding API. Isso garante:

- ✅ Precisão geográfica
- ✅ Suporte a múltiplas cidades
- ✅ Facilidade de manutenção
- ✅ Escalabilidade

## 🚨 Tratamento de Erros

A API implementa tratamento robusto de erros:

| Código | Situação |
|--------|----------|
| **200** | Requisição bem-sucedida |
| **400** | Requisição inválida (ex: sigla de estado com mais de 2 caracteres) |
| **404** | Recurso não encontrado (ex: cidade inexistente) |
| **503** | Serviço indisponível (serviços externos offline) |

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação interativa em `/docs` ou verifique os testes em `tests/test_api.py`.

## 📄 Licença

Este projeto é fornecido como está, sem garantias.

---

**Desenvolvido com ❤️ usando FastAPI**
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
