import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Response
from datetime import datetime
from typing import Generator

from permit_scraper.config import get_config
from permit_scraper.items import PermitScraperItem
from permit_scraper.utils import headers

config = get_config()

class ScrapeSpider(scrapy.Spider):
    name: str = "scrape"
    api_url = config.API_URL

    def __init__(self, date=None, *args, **kwargs) -> None:
        super(ScrapeSpider, self).__init__(*args, **kwargs)
        self.date = datetime.strptime(date, '%m-%d-%Y') if date else None

    def start_requests(self) -> Generator[scrapy.Request, None, None]:

        yield scrapy.Request(url=self.api_url, callback=self.parse, headers=headers)

    def parse(self, response: Response):
        if response.status == 403:
            self.logger.error('403 Forbidden: The server blocked the request.')
            return
        
        data: Response = response.json()
        permits = data['result']['records']

        for permit in permits:
            issue_date = datetime.strptime(permit['issued_date'], '%Y-%m-%d %H:%M:%S+00')
            if self.date and issue_date < self.date:
                continue

            loader = ItemLoader(item=PermitScraperItem())
            loader.add_value('permit_number', permit['permitnumber'])
            loader.add_value('worktype', self.normalize(permit['worktype']))
            loader.add_value('status', self.normalize(permit['status']))
            loader.add_value('occupancytype', self.normalize(permit['occupancytype']))
            loader.add_value('declared_valuation', float(permit['declared_valuation'].replace('$', '').replace(',', '')))
            loader.add_value('total_fees', float(permit['total_fees'].replace('$', '').replace(',', '')))
            loader.add_value('issue_date', issue_date.isoformat())
            expiration_date = datetime.strptime(permit['expiration_date'], '%Y-%m-%d %H:%M:%S+00')
            loader.add_value('expiration_date', expiration_date.isoformat())
            loader.add_value('permit_type_description', permit['permittypedescr'])
            loader.add_value('description', permit['description'])
            loader.add_value('comments', permit['comments'])
            loader.add_value('applicant', permit['applicant'])
            loader.add_value('sq_feet', permit['sq_feet'])
            loader.add_value('address', permit['address'])
            loader.add_value('city', permit['city'])
            loader.add_value('state', permit['state'])
            loader.add_value('zip', permit['zip'])
            loader.add_value('property_id', permit['property_id'])
            loader.add_value('parcel_id', permit['parcel_id'])
            loader.add_value('gps_y', permit['gpsy'])
            loader.add_value('gps_x', permit['gpsx'])
            loader.add_value('latitude', permit['y_latitude'])
            loader.add_value('longitude', permit['x_longitude'])

            yield loader.load_item()

        if data['result'].get('links', {}).get('next'):
            next_page = data['result']['links']['next']
            yield response.follow(next_page, self.parse)

    def normalize(self, value):
        return value.strip().title()
