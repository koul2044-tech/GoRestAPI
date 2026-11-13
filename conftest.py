import os
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def api_headers():
    """Фиксура которая возвращает общие заголовки для запросов к GoRest API"""
    token = os.getenv("GOREST_TOKEN")

    if not token:
        raise ValueError("GOREST_TOKEN Не найден")

    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
