from dataclasses import dataclass


@dataclass
class Config:
    image_type: str = ""


def get_config() -> Config:
    return Config()
