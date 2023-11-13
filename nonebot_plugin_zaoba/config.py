from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    morning_hour: int = 7
    morning_minute: int = 0
    evening_hour: int = 23
    evening_minute: int = 0
    morning_send: bool = True
    evening_send: bool = True
