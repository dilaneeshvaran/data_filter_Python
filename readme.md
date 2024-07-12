1) Create Virutal Environment : python -m venv .venv
2) Activate Virtual Environment :
Linux/Max `source .venv/bin/activate`
Windows `.venv\Scripts\activate`

3) Load Data : `python main.py load --input ../data/input/data.csv --format csv`
(add .json/.csv to input folder and change the file name in the command to replace data)

4) Filter Data : `python main.py filter --criteria Spotify Streams>10000`

5) Sort Data : `python main.py sort --sort_key Track`

6) Save Data : `python main.py save --output ../data/output/output.json --format json`
(save format can be csv or json)
