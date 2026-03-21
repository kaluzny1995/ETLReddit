import json
from pydantic import BaseModel


class MongoConnectionConfig(BaseModel):
    """ MongoDB connection config """

    username: str
    password: str
    host: str
    port: int
    database: str
    collection: str

    class ConfigDict:
        frozen = True

    @staticmethod
    def from_json() -> 'MongoConnectionConfig':
        with open("mongo_config.json", "r") as f:
            config = MongoConnectionConfig(**json.load(f))
        return config

    @staticmethod
    def get_db_connection_string() -> str:
        mcc = MongoConnectionConfig.from_json()
        return f"mongodb://{mcc.username}:{mcc.password}@{mcc.host}:{mcc.port}/?authMechanism=DEFAULT"

    @staticmethod
    def get_default_database_name() -> str:
        mcc = MongoConnectionConfig.from_json()
        return mcc.database

    @staticmethod
    def get_default_collection_name() -> str:
        mcc = MongoConnectionConfig.from_json()
        return mcc.collection
