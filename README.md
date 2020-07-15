# FutureTimeline.net categorizer

## How to use
### 1. Collect results from futuretimeline.ne
Assumed: you have nodejs installed
1. go to `scraper`
2. run `npm install cheerio axios`
3. run `node futileAxios.js`
4. This will produce `scraped-axios.json`

### 2. Categorise using LSA
Assumed: you have python installed
1. go to `categorizer/LSA/LSA_py`
2. copy `scraped-axios.json` from above into LSA_py
3. run `python cleaner.py` to get `clean-axios.json`
4. `pip install sklearn nltk gensim`
5. run `python lsaer.py`
6. This will produce `output.csv`

### 3. Generate MDS plot
1. make sure `output.csv` exists
2. run `python mds.py`
3. This will produce a window with a graph.