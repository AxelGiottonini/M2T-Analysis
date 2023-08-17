# 0. Create the fa files from the sequence database
#python ./src/csv_to_fa.py data/base.csv

# 1. Create the 3D structure from the base sequence with OmegaFold
#for f in ./data/base/*.fa; do
#    python ./OmegaFold/main.py $f ./tmp/struct_OmegaFold/
#done

# 2. Create the 3D structure from the base sequence with OpenFold
# TODO

# 3. Compute the analysis
for f in ./data/inference.random.*.csv; do
    python main.py data/base.csv $f
done
    
