import typing
from dataclasses import dataclass

@dataclass
class BaseStatsOutput():
    alignment: typing.Optional[list[str]]
    mutations: typing.Optional[list[tuple[str, int, str]]]
    n_mutations: typing.Optional[int]=None

class BaseStats():
    def __init__(self, sequence_a, sequence_b):
        self.sequence_a = list(sequence_a)
        self.sequence_b = list(sequence_b)

        if len(self.sequence_a) != len(self.sequence_b):
            raise ValueError(f"Sequences length does not match, current values: {len(self.sequence_a)}, {len(self.sequence_b)}")

        self()

    def __call__(self):
        self._alignment = [":" if a == b else " " for a, b in zip(self.sequence_a, self.sequence_b)]
        self._mutations = [(a, i+1, b) for i, (a, b) in enumerate(zip(self.sequence_a, self.sequence_b)) if not a == b]

    @property
    def alignment(self):
        return ''.join(self.sequence_a) + "\n" +\
               ''.join(self._alignment) + "\n" +\
               ''.join(self.sequence_b)

    @property
    def n_mutations(self):
        return sum(not el == ":" for el in self._alignment)

    @property
    def result(self):
        return BaseStatsOutput(
            alignment=self.alignment,
            mutations=self._mutations,
            n_mutations=self.n_mutations,
        )
    
if __name__ == "__main__":
    print(BaseStats(
        "MVPVLRRCLIPPGRSKPGRDVDYPREKPAREPPFRLAFFNRLSY",
        "MVPVLRRCLIPPGRSKPGRDVDYPREKPAREPPFRLAFFNRLSY"
    ).result)