import json
from typing import Optional

import scrapy


class CentrisPlexSpider(scrapy.Spider):
    name = "centris-plex"

    position = {"startPosition": 0}

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.centris.ca/fr/plex~a-vendre~montreal-saint-laurent",
            callback=self.load_results,
        )

    def load_results(self, response):
        yield scrapy.Request(
            url="https://www.centris.ca/Property/GetInscriptions",
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(self.position),
            callback=self.parse_results,
        )

    def parse_results(self, response):
        resp_dict = json.loads(response.body)
        result = resp_dict.get("d").get("Result")

        html = result.get("html")
        # look for class property-thumbnail-summary-link
        sel = scrapy.Selector(text=html)
        listings = sel.css(".property-thumbnail-summary-link::attr(href)").getall()
        for listing in listings:
            url = "https://www.centris.ca" + listing
            yield scrapy.Request(
                url=url,
                callback=self.parse_property_details,
            )

        count = result.get("count")
        increment_num = result.get("inscNumberPerPage")

        if self.position["startPosition"] <= count:
            self.position["startPosition"] += increment_num
            yield scrapy.Request(
                url="https://www.centris.ca/Property/GetInscriptions",
                method="POST",
                body=json.dumps(self.position),
                headers={"Content-Type": "application/json"},
                callback=self.parse_results,
            )

    # https://www.centris.ca/fr/triplex~a-vendre~montreal-saint-laurent/15096301?view=Summary
    def parse_property_details(self, response):
        last_part = response.url.split("/")[-1]

        address = clean_text(response.css("h2[itemprop=address]::text").get())
        price = clean_text(response.css("#BuyPrice::text").get())

        # caracteristics
        def get_div_next_to_text(text: str):
            sanitized_text = text.replace('"', '"')
            return response.xpath(
                f'//div[contains(text(), "{sanitized_text}")]/following-sibling::div'
            )

        characteristic_names = [
            "Année de construction",
            "Superficie du terrain",
            "Stationnement total",
            "Nombre d'unités",
            "Unités résidentielles",
            "Revenus bruts potentiels",
        ]
        characteristics = {
            name: clean_text(get_div_next_to_text(name).css("span::text").get())
            for name in characteristic_names
        }

        def get_financial_details():
            table = response.css(".financial-details-table > table > tbody")
            rows = table.css("tr")
            return {
                name: value
                for row in rows
                if (name := clean_text(row.css("td:nth-child(1)::text").get()))
                and (value := clean_text(row.css("td:nth-child(2)::text").get()))
            }

        financial_details = get_financial_details()

        property_id = last_part.split("?")[0]
        yield {
            "property_id": property_id,
            "address": address,
            "price": price,
            "characteristics": characteristics,
            "financial_details": financial_details,
        }


def clean_text(text: Optional[str]):
    if text is None:
        return None
    return text.strip().replace("\xa0", "")
