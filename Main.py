import requests
from bs4 import BeautifulSoup
import json
import time

INSTOCK = []

WEBHOOK = 'YOUR_WEBHOOK'

def scrape_site(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42'}
    html = requests.get(url=url, headers=headers)
    output = json.loads(html.text)
    print(output)
    return output['products']

# def discord_webhook(title, price, item_url):
#     link = 'https://www.nike.com.br/snkrs' + item_url
#     data = {
#         'embeds': [{
#             'title': title,
#             'fields': [
#                 {'name': 'Preço', 'value': str(price)},
#                 {'name': 'Preço', 'value': str(link)},
#             ]
#         }]
#     }
#     result = requests.post(WEBHOOK, data=json.dumps(data), headers={'Content-type': 'application/json'})
#     print(result.status_code)
    
def discord_webhook(title, price, item_url):
    link = 'https://www.nike.com.br/snkrs' + item_url
    data = {
        'embeds': [
            {
                'type': 'rich',
                'color': 0x00ff00,
                'author': {
                    'name': '',
                },
                'fields': [
                    {
                        'name': f' Nome:',
                        'value': f'```{title}```'
                    },
                    {
                        'name': f' Preço:',
                        'value': f'```{price}```\n[Link de acesso!]({link})'
                    }
                ]
            }
        ]
    }
    result = requests.post(WEBHOOK, data=json.dumps(data), headers={'Content-type': 'application/json'})
    print(result.status_code)



def comparison(item, start):
    if (item['id'] in INSTOCK) and (item['status'] != 'available'):
        INSTOCK.remove(item['id'])
    elif (item['id'] not in INSTOCK) and (item['status'] == 'available') and (item['details']['hasStock'] == True):
        INSTOCK.append(item['id'])
        if start == 0:
            discord_webhook(
                title=item['name'],
                price=item['price'],
                item_url=item['url'])



start = 0
urls = [
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=1&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=2&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=3&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=4&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=5&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=6&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=7&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=8&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=9&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=10&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=11&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance',
    'https://apigateway.nike.com.br/nike-bff/search/snkrs/feed?page=12&resultsPerPage=30&sorting=relevance&scoringProfile=scoreByRelevance'
]

while True:
    for url in urls:
        products = scrape_site(url)
        for product in products:
            comparison(product, start)

    start = 0

    time.sleep(5)
