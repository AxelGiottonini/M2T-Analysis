from dataclasses import dataclass
import os
import typing
import requests
import json
import time

from utils import safe_open, prune_dict
from biosig import Biosig

if not os.path.isdir("./tmp"):
    os.mkdir("./tmp")

@dataclass
class DDMutOutput:
    prediction: typing.Optional[float]
    single_predictions: typing.Optional[list[float]]
    sum_single_predictions: typing.Optional[float]
    avg_distance: typing.Optional[float]

class DDMut(Biosig):
    _prefix = "ddmut"
    API_ENDPOINT = "https://biosig.lab.uq.edu.au/ddmut/api/prediction_mm"

    def __init__(
        self,
        reverse: typing.Optional[bool]=False,
        *args: typing.Any,
        **kwargs: typing.Any
    ):
        super().__init__(*args, **kwargs)
        self.reverse = reverse
        self()

    def __call__(self):
        res = requests.post(
            url = self.API_ENDPOINT,
            data = prune_dict({
                'pdb_accession': self.pdb_accession,
                'reverse': self.reverse
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
        return DDMutOutput(
            prediction=float(result["prediction"]),
            single_predictions=[float(el) for el in result["single_predictions"].split(";")],
            sum_single_predictions=float(result["sum_single_predictions"]),
            avg_distance=float(result["avg_distance"])
        )

if __name__ == "__main__":
    print(DDMut(mutations_list=[("H", 62, "P"), ("T", 40, "A")], pdb_accession="2RN2").result)