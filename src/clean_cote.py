import re
from dataclasses import dataclass
from typing import Literal

IDNO_PATTERN = re.compile(r"\d+.*")

_DEPARTMENTS = Literal["Arsenal", "Manuscrits"]


@dataclass
class ParsedCote:
    input: str
    idno: str | None = None
    dept: _DEPARTMENTS = "Manuscrits"


class CoteCleaner:
    @classmethod
    def get_idno(cls, input: str) -> str | None:
        match = IDNO_PATTERN.search(input)
        if not match:
            print("Error parsing the cote")
        else:
            return match[0].strip()

    @classmethod
    def make_arsenal_cote(cls, idno: str) -> str:
        return f"Ms-{idno}"

    @classmethod
    def make_francais_cote(cls, idno: str) -> str:
        return f"Français {idno}"

    @classmethod
    def make_naf_cote(cls, idno: str) -> str:
        return f"NAF {idno}"

    @classmethod
    def make_nal_cote(cls, idno: str) -> str:
        return f"NAL {idno}"

    @classmethod
    def parse_dept(cls, input: str) -> ParsedCote:
        if "arsenal" in input.lower():
            return ParsedCote(input=input, dept="Arsenal")
        else:
            return ParsedCote(input=input)

    @classmethod
    def clean(cls, input: str) -> ParsedCote:
        pc = cls.parse_dept(input=input)
        pc.idno = cls.get_idno(input=pc.input)
        if pc.idno:
            # All manuscripts in Bibliothèque de l'Arsenal
            if pc.dept == "Arsenal":
                pc.idno = cls.make_arsenal_cote(idno=pc.idno)
            else:
                # Français manuscripts in Dept. Manuscrits
                if (
                    "fr " in pc.input.lower()
                    or "fr." in pc.input.lower()
                    or "français" in pc.input.lower()
                ):
                    pc.idno = cls.make_francais_cote(idno=pc.idno)
                # Nouvelles acquisitions manuscripts in Dept. Manuscrits
                elif (
                    "naf" in pc.input.lower()
                    or "n.a.f." in pc.input.lower()
                    or "nouvelles acquisitions françaises" in pc.input.lower()
                ):
                    pc.idno = cls.make_naf_cote(idno=pc.idno)
                # Nouvelles acquisitions latines in Dept. Manuscrits
                elif (
                    "nal" in pc.input.lower()
                    or "n.a.l." in pc.input.lower()
                    or "nouvelles acquisitions latines" in pc.input.lower()
                ):
                    pc.idno = cls.make_nal_cote(idno=pc.idno)
        return pc
