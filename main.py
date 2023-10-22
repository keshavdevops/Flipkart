from bs4 import BeautifulSoup
import requests
from Data import flipkart_scrapy
import pandas as pd
from urllib import request

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'}
link =  ('https://www.flipkart.com/jewellery-sets/ragabandha-design-studio~brand/pr?sid=mcr%2C96v%2Cyx2&mar'
        'ketplace=FLIPKART&otracker=product_breadCrumbs_RAGABANDHA+DESIGN+STUDIO+Jewellery+Sets')

data = []
pages = int(input(' how many pages you want to scrape :- '))
product_no = 1

for page in range(1, pages + 1):
    url = link + '&page=' + str(page)
    print(url)


    try:
        webpage = requests.get(url, headers=headers)
        if webpage.status_code == 200:
            soup = BeautifulSoup(webpage.content, 'lxml')
            products = soup.find_all('a', attrs={'class': '_2UzuFa'})

            print(f'''\n.................................\n
            this is page {page} total products {len(products)}
            \n.................................\n''')

            for product in products:
                print(f'\nproduct number :- {product_no}')
                product_link = 'https://www.flipkart.com' + product.get('href')

                data.extend(flipkart_scrapy(product_link, f'group{product_no}'))

                product_no += 1
        else:
            print(f"Failed to get html page. Status code: {webpage.status_code}")
    except Exception as e:
        print('your error is \n\n', e)


unique_data = []
for item in data:
    if item not in unique_data:
        unique_data.append(item)



file_name = 'ragabandha-design-studio'
df = pd.DataFrame(data)
df.to_excel(f'/home/keshav/Downloads/flipkart/products_data/{file_name}.xlsx')
print(f'save file {file_name}.xlsx')
