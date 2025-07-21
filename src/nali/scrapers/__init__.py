from ..enums import School

from .template import TemplateScraper
from .hansung import HansungScraper


def get_scraper(school: School):
    scrapers = {
        School.TEMPLATE: TemplateScraper,
        School.HANSUNG: HansungScraper,
        # Add new scraper mappings here
    }

    return scrapers.get(school)()
