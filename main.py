import sys
import os
import pandas as pd

from joblib import Parallel, delayed

from src import BaseStats, DDMut, Maestro

def summary_stats(i, base, mutated):
    base_stats = BaseStats(base, mutated).result
    ddmut = DDMut(mutations_list=base_stats.mutations, pdb_file=f"./tmp/struct_OmegaFold/sequence_{i}.pdb").result
    maestro = Maestro(mutations_list=base_stats.mutations, pdb_file=f"./tmp/struct_OmegaFold/sequence_{i}.pdb").result

    return ", ".join([str(base_stats.n_mutations), str(ddmut.prediction), str(maestro.score), str(maestro.dscore), str(maestro.ddg)])
    

if __name__ == "__main__":

    base_sequences = pd.read_csv(sys.argv[1]).iloc[:,-1]
    mutated_sequences = pd.read_csv(sys.argv[2]).iloc[:,-1]

    out_file = os.path.join("./out", os.path.basename(sys.argv[2])[:-4] + ".stats.csv")

    if not os.path.isdir("./out"):
        os.mkdir("./out")

    columns = ["n_mutations", "ddmut_prediction", "maestro_score", "maestro_dscore", "maestro_ddg"]

    out = columns + Parallel(n_jobs=40)(delayed(summary_stats)(i, base, mutated) for i, (base, mutated) in enumerate(zip(base_sequences, mutated_sequences)) if len(base) == len(mutated))

    #for i, (base, mutated) in tqdm(enumerate(zip(base_sequences, mutated_sequences))):
    #    if len(base) != len(mutated):
    #        continue
    #
    #    base_stats = BaseStats(base, mutated).result
    #    ddmut = DDMut(mutations_list=base_stats.mutations, pdb_file=f"./tmp/struct_OmegaFold/sequence_{i}.pdb").result
    #    maestro = Maestro(mutations_list=base_stats.mutations, pdb_file=f"./tmp/struct_OmegaFold/sequence_{i}.pdb").result
    #
    #    out.append(", ".join([str(base_stats.n_mutations), str(ddmut.prediction), str(maestro.score), str(maestro.dscore), str(maestro.ddg)]))

    out = "\n".join(out)
    with open(out_file, "w") as f:
        f.write(out)


