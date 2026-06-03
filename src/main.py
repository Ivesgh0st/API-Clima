"""
API de Informações de Cidades e Clima
Endpoints para obter informações de clima, cidades por estado e verificar saúde da API
"""

<<<<<<< HEAD
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
from datetime import datetime, timezone
from typing import Optional

import urllib.parse

=======
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging
from typing import Optional

>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Weather API",
    description="API para obter informações de clima e cidades brasileiras",
    version="1.0.0"
)

<<<<<<< HEAD
# Habilitar CORS para permitir requisições de navegadores (Requisito 8)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

=======
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
# URLs das APIs externas
BRASIL_API_BASE = "https://brasilapi.com.br/api"
OPEN_METEO_BASE = "https://geocoding-api.open-meteo.com/v1"
OPEN_METEO_FORECAST = "https://api.open-meteo.com/v1"

# Timeout para requisições
TIMEOUT = 10

<<<<<<< HEAD
# Mapeamento de siglas de estados para nomes extensos (usado na filtragem de geocodificação)
UF_TO_STATE_NAME = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
    "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins"
}


def get_current_timestamp() -> str:
    """
    Retorna o timestamp atual formatado no padrão ISO 8601 UTC (ex: 2025-03-15T14:30:00Z)
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


async def get_city_by_name_brasilapi(city_name: str) -> Optional[dict]:
    """
    Busca a cidade pelo nome na Brasil API (CPTEC) para obter o nome oficial e UF
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            escaped_city = urllib.parse.quote(city_name)
            response = await client.get(f"{BRASIL_API_BASE}/cptec/v1/cidade/{escaped_city}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                # Retorna o primeiro resultado exato/próximo
                return data[0]
            return None
    except Exception as e:
        logger.error(f"Erro ao buscar cidade '{city_name}' na Brasil API: {str(e)}")
        # Propaga a exceção para que o endpoint trate como serviço externo indisponível
        raise e


async def get_coordinates(city_name: str, state_uf: str) -> Optional[dict]:
    """
    Busca as coordenadas de uma cidade usando Open-Meteo Geocoding API e filtra pela UF
=======

async def get_coordinates(city_name: str) -> Optional[dict]:
    """
    Busca as coordenadas de uma cidade usando Open-Meteo Geocoding API
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(
                f"{OPEN_METEO_BASE}/search",
                params={
                    "name": city_name,
                    "country": "Brazil",
                    "language": "pt",
<<<<<<< HEAD
                    "limit": 10
=======
                    "limit": 1
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
                }
            )
            response.raise_for_status()
            data = response.json()
<<<<<<< HEAD
            results = data.get("results", [])
            
            if not results:
                return None
            
            # Tentar filtrar pelo estado correspondente para precisão geográfica
            state_name = UF_TO_STATE_NAME.get(state_uf.upper(), "")
            coords = None
            for res in results:
                res_admin = res.get("admin1", "")
                if state_name and state_name.lower() in res_admin.lower():
                    coords = res
                    break
            
            # Fallback para o primeiro resultado se o filtro por estado falhar
            if not coords:
                coords = results[0]
                
            return {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"]
            }
    except Exception as e:
        logger.error(f"Erro ao buscar coordenadas para {city_name} ({state_uf}): {str(e)}")
        raise e
=======
            
            if not data.get("results"):
                return None
            
            result = data["results"][0]
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "admin1": result.get("admin1", "")
            }
    except Exception as e:
        logger.error(f"Erro ao buscar coordenadas para {city_name}: {str(e)}")
        return None
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601


async def get_weather(latitude: float, longitude: float) -> Optional[dict]:
    """
    Busca informações de clima usando Open-Meteo API
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(
                f"{OPEN_METEO_FORECAST}/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": True,
                    "daily": "temperature_2m_max,temperature_2m_min,weathercode",
                    "timezone": "America/Sao_Paulo"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current_weather", {})
            daily = data.get("daily", {})
            
<<<<<<< HEAD
            weather_code = current.get("weathercode") if current.get("weathercode") is not None else current.get("weather_code", 0)
            weather_description = get_weather_description(weather_code)
            
            temp_min = daily.get("temperature_2m_min", [None])[0]
            temp_max = daily.get("temperature_2m_max", [None])[0]
            
            # Converter para inteiro conforme o formato do exemplo se valores existirem
            if temp_min is not None:
                temp_min = int(round(temp_min))
            if temp_max is not None:
                temp_max = int(round(temp_max))
                
            return {
                "temperatura_min": temp_min,
                "temperatura_max": temp_max,
                "condicao": weather_description
            }
    except Exception as e:
        logger.error(f"Erro ao buscar clima para lat={latitude}, lon={longitude}: {str(e)}")
        raise e
=======
            # Mapear código de clima para descrição
            weather_code = current.get("weathercode", 0)
            weather_description = get_weather_description(weather_code)
            
            return {
                "temperature": current.get("temperature"),
                "temperature_max": daily.get("temperature_2m_max", [None])[0],
                "temperature_min": daily.get("temperature_2m_min", [None])[0],
                "weather_code": weather_code,
                "weather_condition": weather_description
            }
    except Exception as e:
        logger.error(f"Erro ao buscar clima: {str(e)}")
        return None
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601


def get_weather_description(code: int) -> str:
    """
<<<<<<< HEAD
    Mapeia código WMO para descrição de clima em português brasileiro
    """
    weather_map = {
        0: "Céu Limpo",
        1: "Principalmente Céu Limpo",
        2: "Parcialmente Nublado",
        3: "Nublado",
        45: "Nevoeiro",
        48: "Nevoeiro com Geada",
        51: "Garoa Leve",
        53: "Garoa Moderada",
        55: "Garoa Densa",
        61: "Chuva Fraca",
        63: "Chuva Moderada",
        65: "Chuva Forte",
        71: "Neve Fraca",
        73: "Neve Moderada",
        75: "Neve Forte",
        77: "Grãos de Neve",
        80: "Pancadas de Chuva Fraca",
        81: "Pancadas de Chuva Moderada",
        82: "Pancadas de Chuva Forte",
        85: "Pancadas de Neve Fraca",
        86: "Pancadas de Neve Forte",
        95: "Tempestade",
        96: "Tempestade com Granizo Fraco",
        99: "Tempestade com Granizo Forte"
=======
    Mapeia código WMO para descrição de clima
    """
    weather_map = {
        0: "Céu limpo",
        1: "Principalmente céu limpo",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Nevoeiro",
        48: "Nevoeiro com geada",
        51: "Garoa leve",
        53: "Garoa moderada",
        55: "Garoa densa",
        61: "Chuva fraca",
        63: "Chuva moderada",
        65: "Chuva forte",
        71: "Neve fraca",
        73: "Neve moderada",
        75: "Neve forte",
        77: "Grãos de neve",
        80: "Pancadas de chuva fraca",
        81: "Pancadas de chuva moderada",
        82: "Pancadas de chuva forte",
        85: "Pancadas de neve fraca",
        86: "Pancadas de neve forte",
        95: "Tempestade",
        96: "Tempestade com granizo fraco",
        99: "Tempestade com granizo forte"
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
    }
    return weather_map.get(code, "Desconhecido")


<<<<<<< HEAD
async def check_external_services() -> dict:
    """
    Verifica a saúde dos serviços externos (Open-Meteo e Brasil API)
    """
    services_status = {}
    
    # Verificar Open-Meteo Geocoding
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(f"{OPEN_METEO_BASE}/search?name=Brasilia&limit=1")
=======
async def get_cities_by_state(uf: str) -> Optional[list]:
    """
    Busca lista de cidades de um estado usando Brasil API
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(
                f"{BRASIL_API_BASE}/ibge/municipios/v1/{uf.upper()}"
            )
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                # A Brasil API retorna {"nome": ..., "codigo_ibge": ...}
                cities = []
                for city in data:
                    if isinstance(city, dict) and city.get("nome"):
                        cities.append({
                            "id": city.get("codigo_ibge"),
                            "name": city.get("nome")
                        })
                return cities
            return data if isinstance(data, list) else None
    except Exception as e:
        logger.error(f"Erro ao buscar cidades do estado {uf}: {str(e)}")
        return None


async def check_external_services() -> dict:
    """
    Verifica a saúde dos serviços externos
    """
    services_status = {}
    
    # Verificar Open-Meteo
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{OPEN_METEO_BASE}/search?name=São Paulo&country=Brazil&limit=1")
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
            services_status["open_meteo"] = response.status_code == 200
    except Exception as e:
        logger.error(f"Erro ao verificar Open-Meteo: {str(e)}")
        services_status["open_meteo"] = False
    
    # Verificar Brasil API
    try:
<<<<<<< HEAD
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(f"{BRASIL_API_BASE}/ibge/municipios/v1/DF")
=======
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{BRASIL_API_BASE}/ibge/municipios/v1/SP")
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
            services_status["brasil_api"] = response.status_code == 200
    except Exception as e:
        logger.error(f"Erro ao verificar Brasil API: {str(e)}")
        services_status["brasil_api"] = False
    
    return services_status


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """
    Verifica a saúde da API e dos serviços externos
<<<<<<< HEAD
    Retorna sempre HTTP 200 (se saudável ou degradado) conforme a especificação.
=======
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601
    """
    services = await check_external_services()
    all_healthy = all(services.values())
    
<<<<<<< HEAD
    response_content = {
        "status": "healthy" if all_healthy else "degraded",
        "versao": "1.0.0",
        "timestamp": get_current_timestamp()
    }
    
    if not all_healthy:
        response_content["motivo"] = "Serviço externo indisponível"
        
    return JSONResponse(status_code=200, content=response_content)
=======
    return JSONResponse(
        status_code=200 if all_healthy else 503,
        content={
            "status": "healthy" if all_healthy else "degraded",
            "services": services
        }
    )
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601


@app.get("/api/v1/clima/{nome_cidade}", tags=["Clima"])
async def get_climate(nome_cidade: str):
    """
<<<<<<< HEAD
    Retorna informações geográficas e climáticas de uma cidade pelo nome
    """
    # 1. Validação de Entrada: Mínimo 2 caracteres
    if not nome_cidade or len(nome_cidade) < 2:
        return JSONResponse(
            status_code=400,
            content={
                "erro": True,
                "codigo": "NOME_INVALIDO",
                "mensagem": "O nome da cidade deve conter pelo menos 2 caracteres",
                "nome_informado": nome_cidade
            }
        )
    
    # 2. Busca na Brasil API (CPTEC) para obter o nome correto e a sigla do estado (UF)
    try:
        city_info = await get_city_by_name_brasilapi(nome_cidade)
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                "servico": "CPTEC"
            }
        )
        
    if not city_info:
        return JSONResponse(
            status_code=404,
            content={
                "erro": True,
                "codigo": "CIDADE_NAO_ENCONTRADA",
                "mensagem": "Nenhuma cidade encontrada com o nome informado",
                "nome_informado": nome_cidade
            }
        )
        
    official_name = city_info.get("nome")
    state_uf = city_info.get("estado")
    
    # 3. Busca de Coordenadas (Open-Meteo Geocoding)
    try:
        coordinates = await get_coordinates(official_name, state_uf)
        if not coordinates:
            # Caso não ache coordenadas mesmo a cidade existindo no cadastro, trata como não encontrada
            return JSONResponse(
                status_code=404,
                content={
                    "erro": True,
                    "codigo": "CIDADE_NAO_ENCONTRADA",
                    "mensagem": "Nenhuma cidade encontrada com o nome informado",
                    "nome_informado": nome_cidade
                }
            )
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                "servico": "Open-Meteo"
            }
        )
        
    # 4. Busca de Clima (Open-Meteo Forecast)
    try:
        weather_info = await get_weather(coordinates["latitude"], coordinates["longitude"])
        if not weather_info:
            return JSONResponse(
                status_code=503,
                content={
                    "erro": True,
                    "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                    "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                    "servico": "Open-Meteo"
                }
            )
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                "servico": "Open-Meteo"
            }
        )
        
    # 5. Retornar resposta de sucesso formatada
    return JSONResponse(
        status_code=200,
        content={
            "nome": official_name,
            "estado": state_uf,
            "clima": {
                "temperatura_min": weather_info["temperatura_min"],
                "temperatura_max": weather_info["temperatura_max"],
                "condicao": weather_info["condicao"],
                "unidades": {
                    "temperatura": "°C"
                }
            },
            "consultado_em": get_current_timestamp()
        }
    )


async def get_cities_by_state(uf: str) -> Optional[list]:
    """
    Busca lista de cidades de um estado usando Brasil API (IBGE)
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BRASIL_API_BASE}/ibge/municipios/v1/{uf.upper()}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Erro ao buscar cidades do estado {uf}: {str(e)}")
        raise e


@app.get("/api/v1/cidades/{sigla_uf}", tags=["Cidades"])
async def get_cities(
    sigla_uf: str, 
    limite: int = Query(default=10, ge=1, le=100)
):
    """
    Lista cidades de um estado específico com paginação (limite)
    """
    # 1. Validação de Entrada: Sigla deve conter exatamente 2 letras
    if len(sigla_uf) != 2 or not sigla_uf.isalpha():
        return JSONResponse(
            status_code=400,
            content={
                "erro": True,
                "codigo": "SIGLA_UF_INVALIDA",
                "mensagem": "A sigla do estado deve conter exatamente 2 letras",
                "sigla_uf_informada": sigla_uf
            }
        )
        
    uf_upper = sigla_uf.upper()
    
    # 2. Obter cidades da Brasil API (IBGE)
    try:
        data = await get_cities_by_state(uf_upper)
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                "servico": "Brasil API"
            }
        )
        
    if data is None:
        return JSONResponse(
            status_code=404,
            content={
                "erro": True,
                "codigo": "UF_NAO_ENCONTRADA",
                "mensagem": "Estado com a sigla informada não foi encontrado",
                "sigla_uf_informada": sigla_uf
            }
        )

    # 3. Formatar lista de cidades
    cities_list = []
    if isinstance(data, list):
        for city in data:
            if isinstance(city, dict) and city.get("nome"):
                cities_list.append({"nome": city.get("nome")})
                
    # Ordenar por nome para consistência
    cities_list.sort(key=lambda c: c["nome"])
    
    # 4. Limitar o resultado
    limited_cities = cities_list[:limite]
    
    # 5. Retornar resposta
    return JSONResponse(
        status_code=200,
        content={
            "uf": uf_upper,
            "quantidade_retornada": len(limited_cities),
            "cidades": limited_cities,
            "consultado_em": get_current_timestamp()
        }
    )
=======
    Retorna informações de clima de uma cidade
    
    - **nome_cidade**: Nome da cidade (ex: São Paulo, Rio de Janeiro)
    
    Retorna: nome, estado, temperatura mínima/máxima e condição climática
    """
    # Buscar coordenadas da cidade
    coordinates = await get_coordinates(nome_cidade)
    
    if not coordinates:
        raise HTTPException(
            status_code=404,
            detail=f"Cidade '{nome_cidade}' não encontrada"
        )
    
    # Buscar clima
    weather = await get_weather(coordinates["latitude"], coordinates["longitude"])
    
    if not weather:
        raise HTTPException(
            status_code=503,
            detail="Erro ao buscar informações de clima"
        )
    
    return {
        "cidade": coordinates["name"],
        "estado": coordinates["admin1"],
        "temperatura_minima": weather["temperature_min"],
        "temperatura_maxima": weather["temperature_max"],
        "condicao_climatica": weather["weather_condition"],
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"]
    }


@app.get("/api/v1/cidades/{sigla_uf}", tags=["Cidades"])
async def get_cities(sigla_uf: str):
    """
    Lista todas as cidades de um estado específico
    
    - **sigla_uf**: Sigla do estado (ex: SP, RJ, MG)
    
    Retorna: Lista de cidades com ID e nome
    """
    # Validar sigla
    if len(sigla_uf) != 2:
        raise HTTPException(
            status_code=400,
            detail="Sigla do estado deve ter 2 caracteres"
        )
    
    cities = await get_cities_by_state(sigla_uf)
    
    if cities is None:
        raise HTTPException(
            status_code=404,
            detail=f"Estado '{sigla_uf.upper()}' não encontrado"
        )
    
    return {
        "estado": sigla_uf.upper(),
        "total_cidades": len(cities),
        "cidades": cities
    }
>>>>>>> d7388e906ca30c17a16c0c06a06e28ffd4653601


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz com informações sobre a API
    """
    return {
        "message": "Weather API - Informações de Cidades e Clima",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "clima": "/api/v1/clima/{nome_cidade}",
            "cidades": "/api/v1/cidades/{sigla_uf}"
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
