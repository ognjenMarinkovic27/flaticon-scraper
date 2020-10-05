from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import os
from time import sleep

driver = webdriver.Firefox()

search_terms = ["settings"]

images = []

if(not os.path.exists('scraped_images')):
    os.mkdir('scraped_images')

for s in search_terms:
    driver.get(f'https://www.flaticon.com/search/2?word={s}&search-type=icons&license=selection&order_by=4&grid=small')
    content = driver.page_source
    soup = BeautifulSoup(content, features='html5lib')
    pages = int(soup.find('span', attrs={'id': 'pagination-total'}).text) 
    for i in range(pages-1):
        for _ in range(100):
            driver.execute_script("window.scrollBy(0, 100)")
        try:
            ad_overlay = driver.find_element_by_xpath('/html/body/div[13]/div')
            driver.execute_script("arguments[0].style.visibilty=hidden", ad_overlay)
        except:
            pass
        sleep(0.5)
        content = driver.page_source
        soup = BeautifulSoup(content)
        for li in soup.findAll('li', attrs={'class':'icon'}):
            imgdiv = li.find('div', attrs={'class':'icon--holder'})
            imgsrc = None
            if(imgdiv):
                img = imgdiv.find('img', attrs={'class':'lzy lazyload--done'})
                if(img):
                    imgsrc = img['src']
                    print(str(li['data-id']) + ':' + str(imgsrc))
                else:
                    print('no img')
            if(imgsrc):
                images.append(imgsrc)
        if i != pages-2:
            next_page_button = driver.find_element_by_xpath('//*[@id="pagination-more"]')
            next_page_button.click()
        print(f'Found {len(images)} so far')
    if(not os.path.exists(f'scraped_images/{s}')):
        os.mkdir(f'scraped_images/{s}')
    for index, src in enumerate(images):
        print('Downloading ' + str(src))
        urllib.request.urlretrieve(str(src), f'scraped_images/{s}/{index}.png')
    print('Number of images downloaded ' + str(len(images)))

