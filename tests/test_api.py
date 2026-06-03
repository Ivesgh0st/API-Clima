"""
Testes automatizados para a API de Clima e Cidades
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

client = TestClient(app)

# ──────────────────────────────────────────────
# Dados simulados (mocks) das APIs externas
# ──────────────────────────────────────────────

MOCK_BRASIL_API_CITY = {
    "nome": "Fortaleza",
    "estado": "CE",
    "id": 224
}

MOCK_COORDINATES = {
    "latitude": -3.7319,
    "longitude": -38.5267
}

MOCK_WEATHER = {
    "temperatura_min": 24,
    "temperatura_max": 32,
    "condicao": "Parcialmente Nublado"
}

MOCK_CITIES = [
    {"nome": "Abaiara", "codigo_ibge": "2300101"},
    {"nome": "Acarape", "codigo_ibge": "2300150"},
    {"nome": "Acaraú", "codigo_ibge": "2300200"},
    {"nome": "Acopiara", "codigo_ibge": "2300300"},
    {"nome": "Aiuaba", "codigo_ibge": "2300408"},
    {"nome": "Alcântaras", "codigo_ibge": "2300507"},
]

MOCK_SERVICES_HEALTHY = {
    "open_meteo": True,
    "brasil_api": True
}


# ──────────────────────────────────────────────
# Testes: /api/v1/health
# ──────────────────────────────────────────────

class TestHealthEndpoint:
    """Testes para o endpoint de saúde"""

    def test_health_check_success(self):
        """Teste de sucesso: API saudável com serviços externos OK"""
        with patch("main.check_external_services", new_callable=AsyncMock) as mock_check:
            mock_check.return_value = MOCK_SERVICES_HEALTHY
            response = client.get("/api/v1/health")
            
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["versao"] == "1.0.0"
        assert "timestamp" in data

    def test_health_check_degraded(self):
        """Teste de erro: API degradada quando serviço externo está fora (retorna HTTP 200 conforme spec)"""
        with patch("main.check_external_services", new_callable=AsyncMock) as mock_check:
            mock_check.return_value = {"open_meteo": False, "brasil_api": True}
            response = client.get("/api/v1/health")
            
        assert response.status_code == 200  # Deve ser 200 segundo a especificação!
        data = response.json()
        assert data["status"] == "degraded"
        assert data["versao"] == "1.0.0"
        assert data["motivo"] == "Serviço externo indisponível"
        assert "timestamp" in data


# ──────────────────────────────────────────────
# Testes: /api/v1/clima/{nome_cidade}
# ──────────────────────────────────────────────

class TestClimateEndpoint:
    """Testes para o endpoint de clima"""

    def test_climate_success_fortaleza(self):
        """Teste de sucesso: obter clima de Fortaleza"""
        with patch("main.get_city_by_name_brasilapi", new_callable=AsyncMock) as mock_city, \
             patch("main.get_coordinates", new_callable=AsyncMock) as mock_coords, \
             patch("main.get_weather", new_callable=AsyncMock) as mock_weather:
            
            mock_city.return_value = MOCK_BRASIL_API_CITY
            mock_coords.return_value = MOCK_COORDINATES
            mock_weather.return_value = MOCK_WEATHER
            
            response = client.get("/api/v1/clima/Fortaleza")

        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Fortaleza"
        assert data["estado"] == "CE"
        assert data["clima"]["temperatura_min"] == 24
        assert data["clima"]["temperatura_max"] == 32
        assert data["clima"]["condicao"] == "Parcialmente Nublado"
        assert data["clima"]["unidades"]["temperatura"] == "°C"
        assert "consultado_em" in data

    def test_climate_city_not_found(self):
        """Teste de erro: cidade não encontrada retorna 404 formatado"""
        with patch("main.get_city_by_name_brasilapi", new_callable=AsyncMock) as mock_city:
            mock_city.return_value = None
            response = client.get("/api/v1/clima/CidadeInexistente")

        assert response.status_code == 404
        data = response.json()
        assert data["erro"] is True
        assert data["codigo"] == "CIDADE_NAO_ENCONTRADA"
        assert data["mensagem"] == "Nenhuma cidade encontrada com o nome informado"
        assert data["nome_informado"] == "CidadeInexistente"

    def test_climate_name_too_short(self):
        """Teste de erro: nome de cidade com menos de 2 caracteres retorna 400 formatado"""
        response = client.get("/api/v1/clima/X")
        
        assert response.status_code == 400
        data = response.json()
        assert data["erro"] is True
        assert data["codigo"] == "NOME_INVALIDO"
        assert "pelo menos 2 caracteres" in data["mensagem"]
        assert data["nome_informado"] == "X"

    def test_climate_weather_service_unavailable(self):
        """Teste de erro: serviço externo indisponível retorna 503 formatado"""
        with patch("main.get_city_by_name_brasilapi", new_callable=AsyncMock) as mock_city:
            # Forçar falha no serviço da Brasil API
            mock_city.side_effect = Exception("Serviço fora do ar")
            response = client.get("/api/v1/clima/Fortaleza")

        assert response.status_code == 503
        data = response.json()
        assert data["erro"] is True
        assert data["codigo"] == "SERVICO_EXTERNO_INDISPONIVEL"
        assert "Não foi possível obter dados" in data["mensagem"]
        assert data["servico"] == "CPTEC"


# ──────────────────────────────────────────────
# Testes: /api/v1/cidades/{sigla_uf}
# ──────────────────────────────────────────────

class TestCitiesEndpoint:
    """Testes para o endpoint de cidades por estado"""

    def test_cities_success_ce(self):
        """Teste de sucesso: listar cidades do Ceará (limite padrão = 10)"""
        with patch("main.get_cities_by_state", new_callable=AsyncMock) as mock_cities:
            mock_cities.return_value = MOCK_CITIES
            response = client.get("/api/v1/cidades/CE")

        assert response.status_code == 200
        data = response.json()
        assert data["uf"] == "CE"
        assert data["quantidade_retornada"] == 6
        assert len(data["cidades"]) == 6
        # A resposta de cada cidade deve conter apenas a chave "nome"
        assert data["cidades"][0] == {"nome": "Abaiara"}
        assert "consultado_em" in data

    def test_cities_success_with_limit(self):
        """Teste de sucesso: listar cidades limitando a quantidade"""
        with patch("main.get_cities_by_state", new_callable=AsyncMock) as mock_cities:
            mock_cities.return_value = MOCK_CITIES
            response = client.get("/api/v1/cidades/CE?limite=3")

        assert response.status_code == 200
        data = response.json()
        assert data["uf"] == "CE"
        assert data["quantidade_retornada"] == 3
        assert len(data["cidades"]) == 3
        assert data["cidades"][0] == {"nome": "Abaiara"}
        assert data["cidades"][1] == {"nome": "Acarape"}
        assert data["cidades"][2] == {"nome": "Acaraú"}

    def test_cities_state_not_found(self):
        """Teste de erro: estado (UF) não encontrado retorna 404 formatado"""
        with patch("main.get_cities_by_state", new_callable=AsyncMock) as mock_cities:
            mock_cities.return_value = None
            response = client.get("/api/v1/cidades/XX")

        assert response.status_code == 404
        data = response.json()
        assert data["erro"] is True
        assert data["codigo"] == "UF_NAO_ENCONTRADA"
        assert "não foi encontrado" in data["mensagem"]
        assert data["sigla_uf_informada"] == "XX"

    def test_cities_invalid_uf_format(self):
        """Teste de erro: sigla de estado inválida retorna 400 formatado"""
        # Teste com tamanho incorreto
        response = client.get("/api/v1/cidades/CEARA")
        assert response.status_code == 400
        data = response.json()
        assert data["erro"] is True
        assert data["codigo"] == "SIGLA_UF_INVALIDA"
        assert "exatamente 2 letras" in data["mensagem"]
        assert data["sigla_uf_informada"] == "CEARA"

        # Teste com números na sigla
        response = client.get("/api/v1/cidades/12")
        assert response.status_code == 400
        data = response.json()
        assert data["erro"] is True
        assert data["codigo"] == "SIGLA_UF_INVALIDA"
        assert data["sigla_uf_informada"] == "12"


# ──────────────────────────────────────────────
# Testes: / (raiz)
# ──────────────────────────────────────────────

class TestRootEndpoint:
    """Testes para o endpoint raiz"""

    def test_root_endpoint(self):
        """Teste do endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])