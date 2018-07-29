# -*- coding: utf-8 -*-

import scrapy
from pyquery import PyQuery as pq
import json
import re
from coastdemo.items import CoastdemoItem


class CoastSpider(scrapy.Spider):
    name = 'coast'
    allowed_domains = ['www.coast-stores.com']
    base_url = 'https://www.coast-stores.com'
    start_urls = ['https://www.coast-stores.com/']
    gbp_usd = 0.00
    gbp_eur = 0.00


    #### PARSE FUNCTIONS ####

    # -- main parse function --
    def parse(self, response):
        category_links = []

        self.get_currencies()

        body = pq(response.body)

        for i in body("a.text-link").items():
            link = str(i.attr("href"))
            # -- avoid 'all ...' sections --
            if link.lower().find("all") < 0:
                # -- get only links with products --
                if link.find("/c/") == 0:
                    category_links.append(link)

        for link in category_links:
            yield scrapy.Request(url=self.base_url+link, 
                                 callback=self.parse_categories)


    # -- parse categories --
    def parse_categories(self, response):
        item_links = []

        body = pq(response.body)

        for i in body("a.product-block__image").items():
            link = str(i.attr("href"))
            item_links.append(link)

        for i in item_links:
            yield scrapy.Request(url=self.base_url+i, 
                                 callback=self.parse_item)


    # -- parse items --
    def parse_item(self, response):
        body = pq(response.body)

        offer_price = self.get_price(body)
        initial_price = self.get_initial_price(body)
        name = self.get_name(body)

        item_parsed = {
            "code": self.get_code(body),
            "name": self.get_name(body),
            "description": self.get_description(body),
            "designer": "Coast",
            "raw_color": self.get_raw_color(body),
            "price": offer_price,
            "currency": self.get_currency(body),
            "sale_discount": self.calculate_discount(offer_price, 
                                                     initial_price),
            "link": response.request.url,
            "item_type": self.get_item_type(name),
            "gender": "F",
            "stock_status": self.get_stock(body),
            "skus": self.get_skus(body),
            "image_urls": self.get_image_links(body),
            "price_usd": self.get_currency_price(offer_price, self.gbp_usd),
            "price_eur": self.get_currency_price(offer_price, self.gbp_eur)
        }

        yield CoastdemoItem(**item_parsed)


    # -- get code --
    def get_code(self, response):
        code = ""

        for i in response("div.info p").items():
            tmpcode = str(i.text())
            if tmpcode.find("Product code:") >= 0:
                tmp = tmpcode.split(":")
                if len(tmp) > 1:
                    code = tmp[1]

        return code


    # -- get description --
    def get_description(self, response):
        return response("div.info p").text()


    # -- get raw color --
    def get_raw_color(self, response):
        return response("ul li.active span").text()

    # -- get name --
    def get_name(self, response):
        return response("h1").text()


    # -- get price --
    def get_price(self, response):
        price = 0.00

        # -- get offer price and currency --
        tmpprice = response("p.prod-content__price strong").eq(0).text()
        if tmpprice <> "":
            price = float(re.sub(u'[£$€]', '', tmpprice, re.UNICODE))

        return price


    # -- get currency --
    def get_currency(self, response):
        currency = "None"

        tmpprice = response("p.prod-content__price strong").eq(0).text()
        if re.match(u'£', tmpprice, re.UNICODE) is not None:
            currency = "GBP"
        if re.match('$', tmpprice) is not None:
            currency = "USD"
        if re.match(u'€', tmpprice, re.UNICODE) is not None:
            currency = "EUR"

        return currency


    # -- get initial price --
    def get_initial_price(self, response):
        initial_price = 0.00

        tmpprice = response("p.prod-content__price del").eq(0).text()
        if tmpprice <> "":
            initial_price = float(re.sub(u'[£$€]', '', tmpprice, 
                                         re.UNICODE))

        return initial_price


    # -- get stock --
    def get_stock(self, response):
        stock = {}

        # -- get out of stock items --
        no_stock = response("li.no-stock").items()

        for i in no_stock:
            size = str(i("a.highlight").text())
            stock[size] = False

        # -- get on stock items --
        on_stock = response("li.stock").items()

        for i in on_stock:
            size = str(i("a.highlight").text())
            stock[size] = True

        return stock


    # -- get sku's --
    def get_skus(self, response):
        skus = []

        # -- get out of stock items --
        no_stock = response("li.no-stock").items()

        for i in no_stock:
            sku = str(i("input").attr("value"))
            skus.append(sku)

        # -- get on stock items --
        on_stock = response("li.stock").items()

        for i in on_stock:
            sku = str(i("input").attr("value"))
            skus.append(sku)

        return skus


    # -- get product image links --
    def get_image_links(self, response):
        image_urls = []

        images = response("img.slideup-animation").items()

        for i in images:
            image_link = str(i.attr("src"))
            image_urls.append(image_link)

        return image_urls


    # -- get price in currency --
    def get_currency_price(self, offer_price, currency_change):
        return round(offer_price * currency_change, 2)


    #### OTHER FUNCTIONS ####

    # -- calculate discount --
    def calculate_discount(self, offer_price, initial_price):
        discount = 0.00

        if initial_price > 0.00:
            discount = round((offer_price * 100.00) / initial_price, 2)

        return discount


    # -- get item type --
    def get_item_type(self, name):
        item_type = "A"
        shoes = ['heels', 'sandal', 'sandals', 'shoes']
        bags = ['bag', 'handbag']
        jewelery = ['necklace', 'earrings', 'bracelet', 'cuff', 'belt']
        accessories = ['fascinator', 'hat', 'clip', 'scarf', 'cards', 
                       'wedding', 'shawl', 'poncho']

        # -- get data to compare --
        product_name = name.lower()

        # -- find type by word --
        for i in shoes:
            if product_name.find(i) >= 0:
                item_type = "S"

        for i in bags:
            if product_name.find(i) >= 0:
                item_type = "B"

        for i in jewelery:
            if product_name.find(i) >= 0:
                item_type = "J"

        for i in accessories:
            if product_name.find(i) >= 0:
                item_type = "R"

        return item_type


    # -- get currencies prices --
    def get_currencies(self):
        # -- get USD price --
        yahoo_url = """
        https://query1.finance.yahoo.com/v7/finance/quote?symbols=GBPUSD%3DX
        """

        result = pq(url=yahoo_url)
        data = json.loads(result.html())
        self.gbp_usd = data['quoteResponse']['result'][0]['regularMarketPrice']

        # -- get EUR price --
        yahoo_url = """
        https://query1.finance.yahoo.com/v7/finance/quote?symbols=GBPEUR%3DX
        """

        result = pq(url=yahoo_url)
        data = json.loads(result.html())
        self.gbp_eur = data['quoteResponse']['result'][0]['regularMarketPrice']

        return



