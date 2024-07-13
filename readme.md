1) Create Virutal Environment : python -m venv .venv
2) Activate Virtual Environment :
Linux/Max `source .venv/bin/activate`
Windows `.venv\Scripts\activate`

3) go to `cd .\scripts\`

4) Load Data : `python main.py load --input ../data/input/data.csv --format csv`
(add .json/.csv to input folder and change the file name in the command to replace data)

5) Filter Data (Spotify Streams above 100k) : `python main.py filter --criteria "Spotify Streams>100000"`
More keys to sort data ('Spotify Streams', 'YouTube Likes', 'TikTok Likes', 'TikTok Views' ...)
6) Sort Data (Spotify Streams Descending) : `python main.py sort --sort_key "Spotify Streams" `

7) Save Data : `python main.py save --output ../data/output/output.json --format json`
(save format can be csv or json)

Project by
*EESHVARAN Dilan
*AHAT Thamila
*KABORE Alassane