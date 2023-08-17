from dataclasses import dataclass
import os
import typing
import requests
import json
import time

from .utils import safe_open, prune_dict
from .biosig import Biosig

if not os.path.isdir("./tmp"):
    os.mkdir("./tmp")

@dataclass
class DynaMut2Output:
    prediction: typing.Optional[float]
    avg_distance: typing.Optional[float]
    sum_ddg: typing.Optional[float]

class DynaMut2(Biosig):
    _prefix = "dynamut2"
    API_ENDPOINT = "https://biosig.lab.uq.edu.au/dynamut2/api/prediction_mm"

    def __init__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any
    ):
        super().__init__(*args, **kwargs)
        self()

    def __call__(self):
        res = requests.post(
            url = self.API_ENDPOINT,
            data = prune_dict({
                'pdb_accession': self.pdb_accession,
            }),
            files = prune_dict({
                'pdb_file': safe_open(self.pdb_file),
                'mutations_list': safe_open(self._mutations_list_to_tmp_file()),

            })
        )
        res = json.loads(res.text)
        self.job_id = res["job_id"]

    @property
    def result(self):
        while self.status == "RUNNING":
            time.sleep(2.5)

        result = json.loads(self._result.text)[self.mutations]
        return DynaMut2Output(
            prediction=float(result["prediction"]),
            avg_distance=float(result["avg_distance"]),
            sum_ddg=float(result["sum_ddg"])
        )

if __name__ == "__main__":
    print(DynaMut2(mutations_list=["H62P", "T40A"], pdb_accession="2rn2").result)