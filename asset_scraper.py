from requests_html import HTMLSession,AsyncHTMLSession,HTML
import json,csv
  
async def get_asset_info(asession,url):
    r = await asession.get(url,timeout=15,verify=False)
    print(f"response status asset data: {r.status_code} *******")
    print("asset data: convert to json")
    r_json = json.loads(r.content)
    asset_data = r_json['data']
    
    # with open(f"crypto_asset_meta.json", "w+") as f:
    #     json.dump(asset_data, f, ensure_ascii=False, indent=2)
    
    asset_symbol = [elem["symbol"] for elem in asset_data]
    asset_symbol_txt = ','.join(asset_symbol)

    asset_info_url = f'https://web-api.coinmarketcap.com/v1/cryptocurrency/info?symbol={asset_symbol_txt}&aux=urls,logo,description,tags,platform,date_added,notice,status'
    res = await asession.get(asset_info_url,timeout=15,verify=False)
    print(f"response status asset data: {r.status_code} *******")
    print("asset data: convert to json")
    res_json = json.loads(res.content)
    asset_info_detail = res_json['data']

    # with open(f"crypto_asset_info.json", "w+") as f:
    #     json.dump(asset_info_detail, f, ensure_ascii=False, indent=2)

    website,logo,description,tags,status = '','','','',''
    
    for elem in asset_data:
        
        if elem["symbol"] in asset_info_detail:
            website = asset_info_detail[elem["symbol"]]["urls"]["website"]
            if website: 
                if website[0]: website = website[0]
            logo = asset_info_detail[elem["symbol"]]["logo"]
            # description = asset_info_detail[elem["symbol"]]["description"]
            tags = asset_info_detail[elem["symbol"]]["tags"]
            if tags:
                if tags[0]: tags = tags[0]
            status = asset_info_detail[elem["symbol"]]["status"]

        asset_info = [
            elem["cmc_rank"],
            elem["id"],
            f"https://coinmarketcap.com/currencies/{elem['slug']}/",
            website,
            logo,
            elem["name"],
            elem["symbol"],
            # description,
            tags,
            status,
            elem["max_supply"],
            elem["circulating_supply"],
            elem["total_supply"],
            elem["quote"]["USD"]["market_cap"],
            elem["quote"]["USD"]["price"],
            elem["quote"]["USD"]["volume_24h"],
            elem["quote"]["USD"]["percent_change_1h"],
            elem["quote"]["USD"]["percent_change_24h"],
            elem["quote"]["USD"]["percent_change_7d"],
            elem["last_updated"],
        ]

        with open(f"crypto_asset_meta.csv","a") as f1:
            csv_writer_1 = csv.writer(f1)
            csv_writer_1.writerow(asset_info)
    
if __name__ == '__main__':
    asession = AsyncHTMLSession()
    url_list = [
      "https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=USD&cryptocurrency_type=all&limit=1000&sort=market_cap&sort_dir=desc&start=1",
    ]
    asession.run( *[lambda url=url: get_asset_info(asession,url) for url in url_list] )
