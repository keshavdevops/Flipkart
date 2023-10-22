from bs4 import BeautifulSoup
import requests

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
#            "Accept-Encoding": "gzip, deflate",
#            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
#            "Connection": "close", "Upgrade-Insecure-Requests": "1", 'Accept-Language': 'en-US, en;q=0.5'}

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'}


def scrape_data(url, group):
    product_webpage = requests.get(url, headers=headers)
    product_soup = BeautifulSoup(product_webpage.content, 'lxml')

    # title, price, MRP ..............................................

    try:
        title = (product_soup.find('span', attrs={"class": 'B_NuCI'}).text.strip().replace
                 ("\xa0\xa0", ""))
    except Exception as e:
        print(e)
        title = ''
    try:
        selling_price = (product_soup.find('div', attrs={'class': '_30jeq3 _16Jk6d'}).text.strip().replace
                         ('₹', '').replace(',', ''))
    except Exception as e:
        print(e)
        selling_price = ''
    try:
        mrp = (product_soup.find('div', attrs={'class': '_3I9_wc _2p6lqe'}).text.strip().replace
               ('₹', '').replace(',', ''))
    except Exception as e:
        print(e)
        mrp = ''

    # product details ...................................

    details = {'Model Number': '', 'Base Material': '', 'Color': '', 'Type': '',
               'Ideal For': '', 'Sales Package': ''}

    product_details = product_soup.find('div', attrs={'class': 'X3BRps'})
    rows = product_details.find_all('div', attrs={'class': 'row'})

    for row in rows:
        row1 = row.find('div', attrs={'class': 'col col-3-12 _2H87wv'}).text.strip()
        row2 = row.find('div', attrs={'class': 'col col-9-12 _2vZqPX'}).text.strip()
        for Detail in details:
            if row1 == Detail:
                details[Detail] = row2

    # Images ...............................................

    imgs = []
    parent_img_tag = product_soup.find('div', attrs={'class': '_3li7GG'})
    is_sub_images = parent_img_tag.find('ul', attrs={'class': '_3GnUWp'})

    if is_sub_images is not None:
        images_tag = is_sub_images.find_all('img', attrs={'class': 'q6DClP'})
        for image_tag in images_tag:
            image_url = image_tag.get('src').replace('128/128', '832/832')
            imgs.append(image_url)
    else:
        image_url = parent_img_tag.find('img', attrs={'class': '_2r_T1I _396QI4'}).get('src')
        imgs.append(image_url)

    images = {f'Image{i+1}': imgs[i] for i in range(len(imgs))}

    product_data = {'Product URL': url,
                    'Tittle': title,
                    'Selling Price': selling_price,
                    'MRP': mrp,
                    'Model Number': details['Model Number'],
                    'Base Material': details['Base Material'],
                    'Color': details['Color'],
                    'Brand Color': details['Color'],
                    'Type': details['Type'],
                    'Ideal For': details['Ideal For'],
                    'Sales Package': details['Sales Package'].replace(',', '||'),
                    'Group': group,
                    **images
                    }
    return product_data


def flipkart_scrapy(url, group):
    pl = []
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, 'lxml')

    parent_variance = soup.find('div', attrs={'class': '_3wmLAA'})

    if parent_variance and parent_variance.find('span', attrs={'id': 'Color'}) is not None:
        parent_variants_tag = parent_variance.find('ul', attrs={'class': '_1q8vHb'})
        variants_tag = parent_variants_tag.find_all('a')
        brands_color = parent_variants_tag.find_all('div', attrs={'class': '_3Oikkn _3_ezix _2KarXJ _31hAvz'})

        print(f'Total product variants {len(variants_tag)}')

        for variant_tag, brand_color in zip(variants_tag, brands_color):
            variant_url = 'https://www.flipkart.com' + variant_tag.get('href')

            product_data = scrape_data(variant_url, group=group)
            product_data['Brand Color'] = brand_color.text.strip()
            print(product_data)
            pl.append(product_data)

    else:
        product_data = scrape_data(url, group=group)
        print(product_data)
        pl.append(product_data)

    return pl


# flipkart_scrapy(url4, 'group1')
