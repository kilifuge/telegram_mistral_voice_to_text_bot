import logging
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str

@dataclass
class LogConfig:
    level: int
    format: str

@dataclass
class MistralSettings:
    token: str
    model: str 
    voice_model: str

@dataclass
class Config:
    bot: TgBot
    log: LogConfig
    mistral: MistralSettings
    
def get_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(token=env('BOT_TOKEN')),
        log=LogConfig(
            level=getattr(logging,env('LOG_LEVEL')),
            format=env('LOG_FORMAT'),
        ),
        mistral=MistralSettings(
            token=env('MISTRAL_TOKEN'),
            model=env('MODEL'),
            voice_model=env('VOICE_MODEL'),
        )
    )