import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

link = 'https://www.flipkart.com/12seasons-paper-yellow-pink-jewellery-set/p/itmfb43675d40747?pid=JWSG6E6NFSWVCZAB&lid=LSTJWSG6E6NFSWVCZABCKY03Z&marketplace=FLIPKART&store=mcr%2F96v%2Fyx2&spotlightTagId=BestsellerId_mcr%2F96v%2Fyx2&srno=b_1_1&otracker=product_breadCrumbs_12SEASONS%20Jewellery%20Sets&fm=organic&iid=952e51a3-94b9-4d3b-844b-cd9bcad92b8a.JWSG6E6NFSWVCZAB.SEARCH&ppt=browse&ppn=browse&ssid=crjhtdicef77t1j41700503301721'

# link = 'https://www.flipkart.com/'
for _ in range(1):
    response = requests.get(link, headers=headers)

    print(response.content)



# from selenium import webdriver
# import time

# driver = webdriver.Firefox()
# for pg in range(1,3):
#     driver.get(link + str(pg))
#     time.sleep(10)
#     page_content = driver.page_source



# # time.sleep(30)

# driver.close()
# driver.quit()


