from typing import List

import util
from model import Vector
from provider import IDbProvider, IDbVectorProvider, MongoProvider


class MongoDbVectorProvider(IDbVectorProvider):
    """ Vectors provider from Mongo database """

    mongo_provider: IDbProvider

    def __init__(self, mongo_provider: IDbProvider | None = None):
        super(MongoDbVectorProvider, self).__init__()
        self.mongo_provider = mongo_provider or MongoProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'vectors' table if not exists """
        self.mongo_provider.create_table_if_not_exists(Vector, table="vectors", schema="reddit")

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of vector of given phrase """
        self.create_if_not_exists()

        file_dates = self.mongo_provider.get_db_engine().get_database("reddit").get_collection("vectors").find({'phrase': {"$eq": phrase}}).distinct("file_date")
        return file_dates

    def get_vectors(self, phrase: str | None = None) -> List[Vector]:
        """ Returns the vectors of given phrase """
        self.create_if_not_exists()

        vector_definitions = self.mongo_provider.get_db_engine().get_database("reddit").get_collection("vectors")
        if phrase is not None:
            vector_definitions = vector_definitions.find({'phrase': {"$eq": phrase}})
        return list(map(lambda vd: Vector(**vd), vector_definitions))

    def insert_vectors(self, vectors: List[Vector], batch_size: int = 100) -> None:
        """ Inserts the vectors into database """
        self.create_if_not_exists()
        vector_definitions = list(map(lambda v: v.model_dump(), vectors))

        entity_chunks = util.chunk_list_equal_size(vector_definitions, batch_size)
        num_inserted = 0
        print("Inserting vectors:")
        self.mongo_provider.get_logger().info("Inserting vectors:")
        for chunk in entity_chunks:
            self.mongo_provider.get_db_engine().get_database("reddit").get_collection("vectors").insert_many(chunk)
            num_inserted += len(chunk)
            print(f"{num_inserted} out of {len(vector_definitions)}")
            self.mongo_provider.get_logger().info(f"{num_inserted} out of {len(vector_definitions)}")
        print("Vectors inserted.")
        self.mongo_provider.get_logger().info("Vectors inserted.")