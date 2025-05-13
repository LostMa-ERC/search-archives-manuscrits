import casanova
import click

from playwright.sync_api import sync_playwright
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
    TextColumn,
)
from rich import print
from src.advanced_search import SearchPage
from src.clean_cote import CoteCleaner


@click.group
def cli():
    pass


@cli.command("cote")
@click.argument("cote")
@click.option("--observe", is_flag=True, default=True)
def stdin(cote: str, observe: bool):
    with (
        sync_playwright() as pw,
        Progress(
            TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
        ) as prog,
    ):
        _ = prog.add_task(f"Searching '{cote}'")
        # Load the search page
        browser = pw.chromium.launch(headless=observe)
        page = browser.new_page()
        search_page = SearchPage(page=page)
        # Parse the input
        parsed_cote = CoteCleaner.clean(input=cote)
        result = search_page(cote=parsed_cote.idno, dept=parsed_cote.dept)
        print(result)


@cli.command("file")
@click.option("-i", "--infile", required=True)
@click.option("-c", "--cote-column", required=True)
@click.option("-o", "--outfile", required=True)
@click.option("--observe", is_flag=True, default=True)
def csv_input(infile: str, outfile: str, cote_column: str, observe: bool):
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
            parsed_cote = CoteCleaner.clean(input=cote)
            if not parsed_cote.idno:
                enricher.writerow(row)
                continue
            result = search_page(cote=parsed_cote.idno, dept=parsed_cote.dept)
            enricher.writerow(
                row,
                add=[
                    parsed_cote.dept,
                    parsed_cote.idno,
                    result.ark,
                    result.page,
                ],
            )
            prog.advance(t)

        browser.close()


if __name__ == "__main__":
    cli()
