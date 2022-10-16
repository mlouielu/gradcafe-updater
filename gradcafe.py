import datetime

import requests
from lxml import etree


BASE_URL = "https://www.thegradcafe.com"
SURVEY_URL = f"{BASE_URL}/survey/"


def make_params(
    q: str = "",
    institution: str = "",
    program: str = "",
    degree: str = "",
    season: str = "",
):
    return {
        "per_page": 250,
        "q": q,
        "institution": institution,
        "program": program,
        "degree": degree,
        "season": season,
        "page": 1,
    }


def parse_page(r: requests.models.Response):
    root = etree.HTML(r.text)
    for col in root.xpath(
        '//*[@id="results-container"]//' '*[contains(@class, "col")]'
    ):
        try:
            top, stat = col.xpath('*[contains(@class, "mt")]')
        except ValueError:
            # Placeholder?
            continue

        full_name = top.text.strip()
        department = full_name.split(",")[0]
        university = " ".join(full_name.split(",")[1:])
        description = "".join(top.xpath("span/text()"))
        added_date = datetime.datetime.strptime(
            " ".join(col.xpath("p/text()")[0].strip().split()[2:]), "%B %d, %Y"
        )

        stats = list(
            map(
                lambda s: s.strip().replace("\n", "").replace("\t", ""),
                stat.xpath("span/text()"),
            )
        )
        decision = stats[0].split()[0]
        received_date = ""
        if decision in ["Accepted", "Rejected"]:
            received_date = datetime.datetime.strptime(
                f"{added_date.year} {' '.join(stats[0].split()[2:])}", "%Y %d %b"
            )
        degree = stats[-1].strip()

        yield {
            "department": department,
            "university": university,
            "description": description,
            "added_date": added_date,
            "decision": decision,
            "received_date": received_date,
            "degree": degree,
            "raw_stats": stats,
        }


def get_results(query: dict, pages: int = 10):
    for page in range(pages):
        query["page"] = page
        r = requests.get(SURVEY_URL, params=query)
        for result in parse_page(r):
            yield result


if __name__ == "__main__":
    get_results(
        make_params(
            institution="Washington University in St. Louis (WashU/WUSTL)",
            program="Computer Science",
            degree="Masters",
            season="",
        ),
        1,
    )
