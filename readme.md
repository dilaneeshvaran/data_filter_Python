# Project Setup and Usage Instructions

1) Create Virutal Environment : `python -m venv .venv`
2) Activate Virtual Environment :
Linux/Max `source .venv/bin/activate`
Windows `.venv\Scripts\activate`

3) Install dependencies `pip install -r requirements.txt`

4) go to `cd .\scripts\`

5) Load Data : `python main.py load --input ../data/input/students/students.csv --format csv`
(add .json/.csv to input folder and change the file name in the command to replace data)

5) Try the commands below to play with the data : 
```python
python main.py filter --criteria "firstname avant lastname"
python main.py filter --criteria "apprentice = true"
python main.py filter --criteria "apprentice = false"
python main.py filter --criteria "age < 20"
python main.py filter --criteria "lastname commence 'D'"
python main.py filter --criteria "lastname finit 'son'"
python main.py filter --criteria "firstname contient 'ane'"
python main.py filter --criteria "name<Monitor"
python main.py stats
python main.py sort --sort_key "lastname,firstname"
```

7) Save Data : `python main.py save --output ../data/output/output.json --format json`
(save format can be csv or json)

Project by
*EESHVARAN Dilan
*ACHAT Thamila
*KABORE Alassane