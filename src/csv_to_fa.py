import os
import pandas as pd

def csv_to_fa(f):
    dir_name = os.path.dirname(f)
    file_name = os.path.basename(f)[:-4]
    out_dir = os.path.join(dir_name, file_name)
    os.mkdir(out_dir)

    df = pd.read_csv(f)
    sequences = df.iloc[:, -1]

    for i in range(len(sequences)):
        with open(os.path.join(out_dir, f"sequence_{i}.fa"), "w") as out:
            out.write(f">sequence_{i}\n{sequences[i]}\n")


if __name__ == "__main__":
    import sys
    csv_to_fa(sys.argv[1])
    sys.exit(0)