# Search the BNF's Archives et Manuscrits

Scraper for using the [Advanced Search](https://archivesetmanuscrits.bnf.fr/pageRechercheAvancee.html) of the BNF's Archives et Manuscrits website.

## Install

1. Create a virtual environment in Python 3.12 (or greater) and activate it.

2. Install this package with `pip install .` (or `uv pip install .` if using [`uv`](https://docs.astral.sh/uv/)).

3. Install [`playwright`](https://playwright.dev/python/docs/library)'s dependencies. Troubleshoot any error messages if your computer is missing a dependency for playwright.

```
playwright install
```

> The Archives et Manuscrits' advanced search does not operate on a Restful API. We need to emulate a browswer in order to run a search. For this reason, we use [`playwright`](https://playwright.dev/python/docs/library), which creates a headless Chrome browser.

## Run

This scraper takes in a shelfmark (_cote_ in French) of manuscripts in the BNF and enriches it with the ARK (Archival Resource Key) and page link for the matching manuscript--if the search produced only one result.

To test it on a single _cote_, simply run the `searcham cote` subcommand with the _cote_ in quotation marks.

```
$ searcham cote "nouvelles acquisitions latines 993"
Searching 'nouvelles acquisitions latines 993' ⠹ 0:00:01
SearchResult(cote='NAL 993', ark='/ark:/12148/cc71638k/cd0e403', page='https://archivesetmanuscrits.bnf.fr/ark:/12148/cc71638k/cd0e403')
```

To run the scraper on a set of _cotes_, run the `searcham file` subcommand on a CSV file containing the _cotes_ with the following parameters:

- `-i` / `--infile` : the path to the CSV file
- `-c` / `--cote-column` : the name of the column in the CSV file that contains the shelfmark (_cote_)
- `-o` / `--outfile` : the path to the enriched CSV that the program will produce / overwrite

```console
searcham -i input.csv -c cote -o output.csv
Scraping ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5/5 0:00:05
```

If you want to observe the Chrome browswer, add the flag `--observe`. This will automatically open a browser window on your machine, which will load and interact with the search page, and it will automatically close when the program has finished.

### Input

Currently, the scraper will only search in the Bibliothèque de l'Arsenal and the Département des Manuscrits (default). If the manuscript is in the Arsenal, be sure to include the word "Arsenal" in the _cote_.

|cote|
|--|
|fr. 96|
|Arsenal 2985|
|"Paris, Bibliothèque de l'Arsenal, 3472"|
|"Paris, Bibliothèque nationale de France, français 1598"|
|NAF 6234|

### Output

For debugging, the department and the exact cote used in the search are listed beside the original data. If the search was successful, the ARK and a link to the manuscript's notice are provided.

|cote|searched_dept|searched_cote|ark|page|
|--|--|--|--|--|
|fr. 96|Manuscrits|Français 96|/ark:/12148/cc51219h|https://archivesetmanuscrits.bnf.fr/ark:/12148/cc51219h|
|Arsenal 2985|Arsenal|Ms-2985|/ark:/12148/cc837150|https://archivesetmanuscrits.bnf.fr/ark:/12148/cc837150|
|"Paris, Bibliothèque de l'Arsenal, 3472"|Arsenal|Ms-3472|/ark:/12148/cc841476|https://archivesetmanuscrits.bnf.fr/ark:/12148/cc841476|
|"Paris, Bibliothèque nationale de France, français 1598"|Manuscrits|Français 1598|/ark:/12148/cc46160s|https://archivesetmanuscrits.bnf.fr/ark:/12148/cc46160s|
|NAF 6234|Manuscrits|NAF 6234|/ark:/12148/cc41016b|https://archivesetmanuscrits.bnf.fr/ark:/12148/cc41016b|
