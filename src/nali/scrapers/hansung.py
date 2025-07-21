import re
from datetime import datetime

from .base import BaseScraper
from ..models import Notice


def is_not_notice(tr):
    cls = tr.get("class")
    return not cls or "notice" not in cls


class HansungScraper(BaseScraper):
    def scrape(self, page: int, search: str | None = None) -> list[Notice]:
        url = "https://hansung.ac.kr/bbs/hansung/143/artclList.do"

        soup = self.fetch_page(url=url, method="POST", data={"page": page, "srchColumn": "sj", "srchWrd": search})

        table_body = soup.find("tbody")

        trs = [tr for tr in table_body.find_all('tr') if is_not_notice(tr)]

        notices = []

        for tr in trs:
            id_ = (int(tr.find("td", class_=lambda x: x == "td-num").text.strip()))
            title = re.sub(r"\s+", " ", tr.find("strong").text.strip())
            author = tr.find("td", class_=lambda x: x == "td-write").text.strip()
            url = "https://hansung.ac.kr" + tr.find("a").get("href") + "?layout=unknown"
            date = datetime.strptime(tr.find("td", class_=lambda x: x == "td-date").text.strip(), "%Y.%m.%d")

            notices.append(Notice(id=id_, title=title, content=None, author=author, url=url, date=date))

        return notices
