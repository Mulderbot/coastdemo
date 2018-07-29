Simple Spider Task
==================

Pre-requisites
--------------
- python 2.7
- scrapy http://scrapy.org/
- pyquery

What you need to do
----
- crawl online retailer www.coast-stores.com for appropriate product pages
- return items representing products
- output in json format

What are we going to check
-----
- following rules
- number of items crawled
- code organization and readability

Instructions
------------
- run "scrapy startproject coastdemo",
- update items.py in coastdemo/coastdemo,
- create coast.py in coastdemo/coastdemo/spiders,
- write crawling rules (these few lines are a big part of the task - you want to crawl the site in an efficient way),
   - to find appropriate category listing pages,
   - to identify individual product pages (this rule should have a callback='parse_item'),
- fill out parse_item method to populate the item's fields (one method per field),
- make sure that prices are in GBP
- don't use `xpath` for getting data, use `pyquery` instead
- (import from standard python libraries where required, but nothing external other than what's already imported),
- run "scrapy crawl coastdemo.com -o items.json -t json",
- when satisfied, upload `coastdemo.py` and `items.json` to gist and send them to us.

Examples
--------
This url: https://www.coast-stores.com/p/mylene-bow-lace-top/1899320 could yield an item dictionary:
```python
{
   "code":"1899320",
   "name":"Mylene Bow Lace Top",
   "description":"The Mylene Bow Lace Top combines classic lace with a modern bodice for a statement look. Team this bridesmaid top with our Amy Skirt or Iridesa Skirt to ensure your bridal party make a very stylish entrance on the big day. Fabric:Main: 97.0% Polyester; 3.0% Elastane. Wash care:Dry Clean.",
   "designer":"Coast",
   "raw_color":"Navy",
   "price": "89.00",
   "currency": "GBP",
   "sale_discount":40.0,
   "link":"https://www.coast-stores.com/p/mylene-bow-lace-top/1899320"
   "type":"A",
   "gender":"F",
   "stock_status":{
         "10":True,
         "12":True,
         "14":True,
         "16":False,
         "18":False,
         "6":True,
         "8":True
   },
   "skus":[
         "5051048834916",
         "5051048834923",
         "5051048834930",
         "5051048834947",
         "5051048834954",
         "5051048834961",
         "5051048834978"
   ],
   "image_urls":[
      "https://coast.btxmedia.com/pws/client/images/catalogue/products/1899320/LG/1899320.jpg",
      "https://coast.btxmedia.com/pws/client/images/catalogue/products/1899320/LG/1899320_1.jpg",
      "https://coast.btxmedia.com/pws/client/images/catalogue/products/1899320/LG/1899320_2.jpg",
      "https://coast.btxmedia.com/pws/client/images/catalogue/products/1899320/LG/1899320_3.jpg",
      "https://coast.btxmedia.com/pws/client/images/catalogue/products/1899320/LG/1899320_4.jpg",
      "https://coast.btxmedia.com/pws/client/images/catalogue/products/1899320/LG/1899320_5.jpg"
   ]
}
```

Field details
-------------
- **type** - try and make a best guess, one of:
  - 'A' apparel
  - 'S' shoes
  - 'B' bags
  - 'J' jewelry
  - 'R' accessories
- **gender**, one of:
  - 'F' female
  - 'M' male
- **designer** - manufacturer of the item
- **code** - unique identifier from a retailer perspective
- **name** - short summary of the item
- **description** - fuller description and details of the item
- **raw_color** - best guess of what colour the item is (set to None if unidentifiable)
- **image_urls** - list of urls of large images representing the item
- **price** - full (non-discounted) price of the item
- **currency** - price currency
- **sale_discount** - percentage discount for sale items where applicable 
- **stock_status** - dictionary of sizes to stock status
  - False - out of stock
  - True - in stock
- **skus** - list of skus
- **link** - url of product page

Extra points
------------

- Get items with prices from any other currency (USD or EUR).

Help
-----------

If you don't know how to start, this is good starting point http://doc.scrapy.org/en/master/topics/spiders.html?highlight=rules#crawlspider-example 