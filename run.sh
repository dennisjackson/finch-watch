mkdir data/
npx finch-trials > data/raw.json
python3 finch-csv.py data/raw.json data/
