import csv
from typing import Any

from permit_scraper.items import PermitScraperItem

class PermitScraperPipeline:

    def open_spider(self, spider: Any) -> None:
        self.file = open(f'output/{spider.name}_permits.csv', 'w', newline='')
        self.exporter = csv.writer(self.file)
        self.exporter.writerow([
            'Permit Number', 'Work Type', 'Status', 'Occupancy Type', 'Declared Valuation', 
            'Total Fees', 'Issue Date', 'Expiration Date', 'Permit Type Description',
            'Description', 'Comments', 'Applicant', 'Sq Feet', 'Address', 'City', 'State', 
            'Zip', 'Property ID', 'Parcel ID', 'GPS Y', 'GPS X', 'Latitude', 'Longitude'
        ])

    def close_spider(self, spider: Any) -> None:
        self.file.close()

    def process_item(self, item: PermitScraperItem, spider: Any) -> PermitScraperItem:
        self.exporter.writerow([
            item.get('permit_number'),
            item.get('worktype'),
            item.get('status'),
            item.get('occupancytype'),
            item.get('declared_valuation'),
            item.get('total_fees'),
            item.get('issue_date'),
            item.get('expiration_date'),
            item.get('permit_type_description'),
            item.get('description'),
            item.get('comments'),
            item.get('applicant'),
            item.get('sq_feet'),
            item.get('address'),
            item.get('city'),
            item.get('state'),
            item.get('zip'),
            item.get('property_id'),
            item.get('parcel_id'),
            item.get('gps_y'),
            item.get('gps_x'),
            item.get('latitude'),
            item.get('longitude')
        ])
        return item
