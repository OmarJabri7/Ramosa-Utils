import requests

from parsel import Selector
import json
import httpx
import pandas as pd


def extract_search(response):
    """extract json data from search page"""
    if type(response) != str:
        sel = Selector(response.text)
    else:
        sel = Selector(response)
    # find script with page data in it
    script_with_data = sel.xpath(
        '//script[contains(text(),"window.runParams")]')
    # select page data from javascript variable in script tag using regex
    return json.loads(script_with_data.re(r"window.runParams\s*=\s*({.+?});")[0])


def parse_search(response):
    """Parse search page response for product preview results"""
    data = extract_search(response)
    parsed = []
    for result in data["mods"]["itemList"]["content"]:
        parsed.append(
            {
                # "id": result["productId"],
                "url": f"https://www.aliexpress.com/item/{result['productId']}.html",
                "type": result["productType"],  # can be either natural or ad
                "title": result["title"]["displayTitle"][:50],
                "price": result["prices"]["salePrice"]["minPrice"],
                "currency": result["prices"]["salePrice"]["currencyCode"],
                # trade line is not always present
                "trade": result.get("trade", {}).get("tradeDesc"),
                "reviews": result.get("evaluation", {}).get("starRating", None),
                # "thumbnail": result["image"]["imgUrl"].lstrip("/"),
                "store": {
                    "url": result["store"]["storeUrl"],
                    "name": result["store"]["storeName"],
                    "id": result["store"]["storeId"],
                    "ali_id": result["store"]["aliMemberId"],
                },
            }
        )
    return parsed


def ali_express_scraper(product):
    # for example, this category is for android phones:
    main_url = f"https://www.aliexpress.com/wholesale?SearchText={product}"
    # f"https://www.alibaba.com/trade/search?SearchText={product}"
    client = httpx.Client(timeout=None)
    resp = client.get(main_url, follow_redirects=True)
    res = dict()
    # with open("ali_express.html", "w") as f:
    #         f.write(resp.text)
    try:
        res = parse_search(resp)
    except Exception as e:
        try:
            if e.__dict__ != {}:
                error = e.__dict__
                delim = error['msg'][error['msg'].find(',')]
                loc = error['colno']
                doc = error['doc'][:loc - 1] + delim + error['doc'][loc-1:]
                res = parse_search(doc)
            else:
                res = parse_search(doc)
        except:
            pass
    return res
