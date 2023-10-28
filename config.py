from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class DatabaseConfig:
    SOCIAL_AUTH_GITHUB_KEY: str
    SOCIAL_AUTH_GITHUB_SECRET: str
    SOCIAL_AUTH_VK_OAUTH2_KEY: str
    SOCIAL_AUTH_VK_OAUTH2_SECRET: str
    DATABASE_PASSWORD: str


@dataclass
class Config:
    db: DatabaseConfig


def load_config(path: Optional[str]) -> Config:
    env: Env = Env()  # Создаем экземпляр класса Env
    env.read_env(path)  # Добавляем в переменные окружения данные, прочитанные из файла .env
    return Config(db=DatabaseConfig(SOCIAL_AUTH_GITHUB_KEY=env('SOCIAL_AUTH_GITHUB_KEY'),
                                    SOCIAL_AUTH_GITHUB_SECRET=env('SOCIAL_AUTH_GITHUB_SECRET'),
                                    SOCIAL_AUTH_VK_OAUTH2_KEY=env('SOCIAL_AUTH_VK_OAUTH2_KEY'),
                                    SOCIAL_AUTH_VK_OAUTH2_SECRET=env('SOCIAL_AUTH_VK_OAUTH2_SECRET'),
                                    DATABASE_PASSWORD=env('DATABASE_PASSWORD')))
