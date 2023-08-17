import typing
import time
import requests
import json

class Biosig():
    _prefix = None
    API_ENDPOINT = None

    def __init__(
        self, 
        mutations_list: typing.Optional[list[tuple[str, int, str]]], 
        pdb_accession: typing.Optional[str]=None, 
        pdb_file: typing.Optional[str]=None
    ):
        self.__time = time.time()
        self.job_id = None

        self.mutations_list = mutations_list
        self.pdb_accession = pdb_accession
        self.pdb_file = pdb_file

        if not (self.pdb_accession is not None) ^ (self.pdb_file is not None):
            raise ValueError()

    def _mutations_list_to_tmp_file(self):
        with open(file_name:=f"./tmp/{self._prefix}_{str(self.__time).replace('.', '')}.txt", "w") as f:
            f.write(self.mutations + "\n")
        return file_name

    @property
    def mutations(self):
        return '; '.join([f"A {el[0]}{el[1]}{el[2]}" for el in self.mutations_list])

    @property
    def _result(self):
        return requests.get(url=self.API_ENDPOINT, data={"job_id":self.job_id})

    @property
    def status(self):
        if self._result.status_code == 500:
            return "SERVER ERROR"

        if self._result.status_code != 200:
            return "FAILED"
        
        result = json.loads(self._result.text)
        if "status" in result.keys():
            return result["status"]
        
        return "COMPLETED"
