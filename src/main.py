import casanova
import click

from playwright.sync_api import sync_playwright
from rich.progress import (
    Progress,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
    TextColumn,
)
from src.advanced_search import SearchPage
from src.clean_cote import clean_cote


@click.command
@click.option("-i", "--infile", required=True)
@click.option("-c", "--cote-column", required=True)
@click.option("-o", "--outfile", required=True)
@click.option("--observe", is_flag=True, default=True)
def main(infile, outfile, cote_column, observe):
    with (
        sync_playwright() as pw,
        open(infile) as f,
        open(outfile, "w") as of,
        Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        ) as prog,
    ):
        # Set up progress bar
        total = casanova.count(infile)
        t = prog.add_task("Scraping", total=total)

        # Load the search page
        browser = pw.chromium.launch(headless=observe)
        page = browser.new_page()
        search_page = SearchPage(page=page)

        # Iterate through the data
        enricher = casanova.enricher(
            f, of, add=["searched_dept", "searched_cote", "ark", "page"]
        )
        for row, cote in enricher.cells(cote_column, with_rows=True):
            cleaned_cote, dept = clean_cote(cote)
            if not cleaned_cote:
                enricher.writerow(row)
                continue
            result = search_page(cote=cleaned_cote, dept=dept)
            enricher.writerow(row, add=[dept, cleaned_cote, result.ark, result.page])
            prog.advance(t)

        browser.close()


if __name__ == "__main__":
    main()
