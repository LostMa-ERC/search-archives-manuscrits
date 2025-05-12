from pydantic import BaseModel, computed_field, Field


class SearchResult(BaseModel):
    cote: str
    ark: str | None = Field(default=None)

    @computed_field
    @property
    def page(self) -> str | None:
        if self.ark:
            return "https://archivesetmanuscrits.bnf.fr" + self.ark
