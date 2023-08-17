# M2T-Analysis

## [DDMut: predicting effects of mutations on protein stability using deep learning](https://academic.oup.com/nar/article/51/W1/W122/7191416)

### Paper Details:
- DDMut can be used to predict $\Delta\Delta G$s for both single point mutations and multiple mutations under two different options. [...] Although the web server does accept submissions for more than three simultaneou smutations, it is important to note that the model has only been validated on up to triple point mutations.

### API (Multiple Mutations Prediction)
#### Post - Job Submission
Arguments
- pdb_accession (optional) - 4 character PDB code
- pdb_file (optional) - file in PDB format
- mutation_list (required) - .txt or .csv file with mutation list. One mutation code per line (aaFrom + residueNumber + aaTo).
- Reverse (optional) - Whtehter ot predict reverse mutations (True/False). Default is False

Return
- job_id - ID used for uniquely identify each job

Examples
- curl
```
$ curl https://biosig.lab.uq.edu.au/ddmut/api/prediction_mm -X POST -i -F pdb_file=@/home/ubuntu/2rn2.pdb -F mutations_list=@/home/ubuntu/mutations.txt
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 33
Date: Wed, 10 Jun 2022 05:10:59 GMT
{
"job_id": "16705686765979645"
}
```

#### Get - Retrieve Job Results
Arguments
- job_id - ID used ofr uniquely identify each job. Generated upon submission.

Return

For jobs still being processed or waiting on queue, the message below will be returned from querying this endpoint:
- message - RUNNING

For jobs successfully processed by ddmut, the following data will be returned:
- Array list of results (in json format) for each mutation identified with a sequencial identifying number

Examples
- curl
```
$ curl https://biosig.lab.uq.edu.au/ddmut/api/prediction_mm -X GET -F job_id=16705686765979645
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 33
Date: Wed, 10 Jun 2022 06:16:53 GMT
{
"A H62P;A T40A;A K122R": {"prediction": 0.45, "single_predictions": "0.43;-0.23;0.18", "sum_single_predictions": 0.38, "avg_distance": 29.67},
"A E119V;A K60R": {"prediction": 0.07, "single_predictions": "0.33;0.11", "sum_single_predictions": 0.46, "avg_distance": 22.12},
"A E119V;A R41C": {"prediction": 1.23, "single_predictions": "0.36;0.16", "sum_single_predictions": 0.51, "avg_distance": 28.61}
}
```

## [DynaMut2: Assessing changes in stability and flexibility upon single and multiple point missense mutations](https://doi.org/10.1002/pro.3942)

### API (Multiple Mutations Prediction)
#### Post- Job Submission
Arguments
- pdb (optional) - 4 character PDB code
- pdb_file (optional) - file in PDB format
- mutation_list (required) - .txt or .csv file with mutation list. One mutation code per line (aaFrom + residueNumber + aaTo).

Return
- job_id - ID used for uniquely identify each job

Examples
- curl
```
$ curl https://biosig.lab.uq.edu.au/dynamut2/api/prediction_mm -X POST -i -F pdb_file=@/home/ubuntu/1u46.pdb -F mutations_list=@/home/ubuntu/mutations.txt
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 33
Date: Wed, 10 Jun 2020 05:10:59 GMT
{
"job_id": "159177154575"
}
```
#### GET - Retrieve Job Results
Arguments
- job_id - ID used for uniquely identify each job. Generated upon submission

Return

For jobs still being processed or waiting on queue, the message below will be returned from querying this endpoint:
- message - RUNNING

For jobs successfully processed by DynaMut2, the following data will be returned:
- Array list of results (in json format) for each mutation indntified with a sequencial identifying number

Examples
- curl
```
$ curl https://biosig.lab.uq.edu.au/dynamut2/api/prediction_mm -X GET -F job_id=159177154575
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 33
Date: Wed, 10 Jun 2020 06:16:53 GMT
{
"A E346K;A T118P": {"avg_distance":"47.18","prediction":"-0.84","sum_ddg":"-0.42"},
}
```

## [MAESTRO -- multi agent stability prediction upon point mutations](https://10.1186/s12859-015-0548-6)

```
#Download [bash commands]
wget https://pbwww.services.came.sbg.ac.at/maestro/v1.2.35/MAESTRO_linux_x64.zip

#Unzip [python commands]
from zipfile import ZipFile
with ZipFile("./MAESTRO_linux_x64.zip", 'r') as z:
    z.extractall("./MAESTRO")

#Change Maestro rights [bash commands]
chmod +x ./MAESTRO/MAESTRO_linux_x64/maestro
```

## OmegaFold
### Install
```
python ./OmegaFold/setup.py install
```
### Run
```
python ./OmegaFold/main.py INPUT_FILE.fasta OUTPUT_DIRECTORY
```