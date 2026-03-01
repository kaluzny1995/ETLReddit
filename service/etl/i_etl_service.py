from abc import ABC, abstractmethod


class IETLService(ABC):
    """ Interface for all ETL services """

    @abstractmethod
    def run_etl(self, **etl_params_dict) -> None:
        """ Runs ETL process loading expected input entries, processing and persisting expected output data """
        pass
