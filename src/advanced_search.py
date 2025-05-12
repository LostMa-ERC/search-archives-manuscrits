from playwright.async_api import Page

from src.search_result import SearchResult
from src.css_selectors import (
    RETURN_BUTTON,
    FIRST_SEARCH_RESULT,
    SEARCH_BUTTON,
    DEPT_MANUSCRITS_BOX,
    BIB_ARSENAL_BOX,
)

URI = "https://archivesetmanuscrits.bnf.fr/pageRechercheAvancee.html"


class SearchPage:

    def __init__(self, page: Page):
        self.page = page
        self.page.goto(URI)

    def get_cote_form(self):
        return self.page.locator("input[id='COTE_INPUT1']")

    def refresh(self):
        # Go back to the search page
        self.page.locator(RETURN_BUTTON).click()

        # Delete the cote
        cote_form = self.get_cote_form()
        cote_form.fill("")

        # Uncheck department boxes
        self.page.locator(BIB_ARSENAL_BOX).uncheck()
        self.page.locator(DEPT_MANUSCRITS_BOX).uncheck()

    def __call__(self, cote: str, dept: str) -> SearchResult:
        # Search for the department's manuscript
        if dept == "Arsenal":
            result = self.run_search(cote=cote, dept_locator=BIB_ARSENAL_BOX)
        else:
            result = self.run_search(cote=cote, dept_locator=DEPT_MANUSCRITS_BOX)

        # Return to the search page and remove the forms' input
        self.refresh()

        # Return the search result
        return result

    def get_result(self) -> str | None:
        # Run the search for the cote
        search_button = self.page.locator(SEARCH_BUTTON)
        search_button.click()

        # Confirm that the cote was found
        result_count_css_selector = "div.paginationBam:nth-child(1) > .text-left"
        result_count = (
            self.page.locator(result_count_css_selector).text_content().strip()
        )
        if result_count == "1 résultat":
            href = self.page.locator(FIRST_SEARCH_RESULT).get_attribute("href")
            ark = href[1:]
            return ark

    def run_search(self, cote: str, dept_locator: str) -> SearchResult:
        cote_form = self.get_cote_form()
        cote_form.fill(cote)
        self.page.locator(dept_locator).check()
        ark = self.get_result()
        return SearchResult(cote=cote, ark=ark)
