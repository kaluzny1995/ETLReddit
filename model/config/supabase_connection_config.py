import json
from pydantic import BaseModel


class SupabaseConnectionConfig(BaseModel):
    """ Supabase connection config """
    username: str
    password: str
    host: str
    port: int
    database: str

    class Config:
        frozen = True

    @staticmethod
    def from_json() -> 'SupabaseConnectionConfig':
        with open("supabase_config.json", "r") as f:
            config = SupabaseConnectionConfig(**json.load(f))
        return config

    @staticmethod
    def get_db_connection_string() -> str:
        scc = SupabaseConnectionConfig.from_json()
        return f"postgresql://{scc.username}:{scc.password}@{scc.host}:{scc.port}/{scc.database}"
