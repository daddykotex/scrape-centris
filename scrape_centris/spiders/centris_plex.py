import json

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
        property_id = last_part.split("?")[0]
        yield {
            "property_id": property_id,
        }
