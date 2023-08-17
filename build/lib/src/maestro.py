import os
from subprocess import check_output
import requests

from dataclasses import dataclass
import typing

import json

if not os.path.isdir("./tmp"):
    os.mkdir("./tmp")

@dataclass
class MaestroOutput:
    score: typing.Optional[float]
    dscore: typing.Optional[float]
    ddg: typing.Optional[float]
    confidence: typing.Optional[float]

class Maestro:
    _prefix = "maestro"
    API_ENDPOINT = "./MAESTRO/MAESTRO_linux_x64/maestro"
    API_CONFIG = "./MAESTRO/MAESTRO_linux_x64/config.xml"

    def __init__(
        self,
        mutations_list: typing.Optional[list[tuple[str, int, str]]],
        pdb_accession: typing.Optional[str]=None,
        pdb_file: typing.Optional[str]=None,
        chain: typing.Optional[str]="A"
    ):
        if not os.path.isfile(self.API_ENDPOINT):
            raise FileNotFoundError(f"Couldn't locate the API ENDPOINT. Current path: {self.API_ENDPOINT}")
        
        self.mutations_list = mutations_list
        self.pdb_accession = pdb_accession
        self.pdb_file = self.__get_pdb_file() if pdb_file is None else pdb_file
        self.chain = chain

        self()

    def __call__(self):
        out = check_output([
            self.API_ENDPOINT,
            self.API_CONFIG,
            self.pdb_file,
            f"--evalmut={self.mutations}",
            "--json"
        ])
        self._result = json.loads(out)

    def __get_pdb_file(self):
        response = requests.get(f"https://files.rcsb.org/download/{self.pdb_accession}.pdb", stream=True)
        with open(path:=os.path.join("./tmp", self._prefix + "_" + self.pdb_accession + ".pdb"), "wb") as handle:
            for data in (response.iter_content()):
                handle.write(data)
        return path

    @property
    def mutations(self):
        return ','.join([f"{el[0]}{el[1]}.{self.chain}{{{el[2]}}}" for el in self.mutations_list])

    @property
    def result(self):
        result = self._result[0]["results"][1]
        return MaestroOutput(
            score=result["score"],
            dscore=result["dscore"],
            ddg=result["ddg"],
            confidence=result["confidence"]
        )

if __name__ == "__main__":
    print(Maestro(mutations_list=[("H", 62, "P"), ("T", 40, "A")], pdb_accession="2RN2").result)