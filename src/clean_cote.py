import re

COTE_PATTERN = re.compile(r"\d+.*")


def clean_cote(cote: str) -> tuple[str, str | None]:
    dept = "Manuscrits"
    match = COTE_PATTERN.search(cote)
    if not match:
        print("Error parsing cote", cote)
        return (None, None)
    else:
        idno = match[0].strip()
        if "arsenal" in cote.lower():
            dept = "Arsenal"
            cleaned_cote = f"Ms-{idno}"
        elif (
            "fr " in cote.lower() or "fr." in cote.lower() or "français" in cote.lower()
        ):
            cleaned_cote = f"Français {idno}"
        elif (
            "naf" in cote.lower()
            or "n.a.f." in cote.lower()
            or "nouvelles acq" in cote.lower()
        ):
            cleaned_cote = f"NAF {idno}"
        else:
            cleaned_cote = idno
    return cleaned_cote, dept
