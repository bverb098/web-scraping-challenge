from tkinter.tix import Tree
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    

def scrape():
    browser=init_browser()
    mars_scrape={}
    #scrape mars news
    mars_news={}
    url_mars_news="https://redplanetscience.com/"
    browser.visit(url_mars_news)
    html_mars_news=browser.html
    soup_mars_news=bs(html_mars_news,'html.parser')
    #obtain first element of list of all news headlines from scrape to get most recent
    latest_news_title=soup_mars_news.find_all("div",class_='content_title')[0].text
    mars_news["headline"]=latest_news_title
    #obtain the paragraph text belonging to the first article
    latest_news_paragraph=soup_mars_news.find_all("div",class_="article_teaser_body")[0].text
    mars_news["paragraph"]=latest_news_paragraph
    #update scrape dictionary
    mars_scrape["news"]=mars_news

    #set up the scrape and beautiful soup object for the mars featured image
    url_mars_image="https://spaceimages-mars.com/"
    browser.visit(url_mars_image)
    html_mars_image=browser.html
    soup_mars_image=bs(html_mars_image,'html.parser')

    #obtain the image url for the featured image
    results=soup_mars_image.find_all("div",class_="floating_text_area")
    for result in results:
        img_path=result.a['href']
        featured_image_url=f"https://spaceimages-mars.com/{img_path}"
    #update scrape dictionary
    featured_image={}
    featured_image["url"]=featured_image_url
    mars_scrape["featured_image"]=featured_image


    #use pandas to get tables off mars facts webpage
    url_mars_facts="https://galaxyfacts-mars.com/"
    planet_profile_table=pd.read_html(url_mars_facts)

    # get the second dataframe from list. NOT the earth/mars comparison
    mars_profile_df=planet_profile_table[1]
    
    #clean dataframe
    mars_profile_df.rename(columns={0:"Item",1:"Fact"},inplace=True)
    mars_profile_df.reset_index
    
    #convert table into html
    html_mars_profile=mars_profile_df.to_html(bold_rows=True,index=False)
    #update scrape dictionary
    mars_table={}
    mars_table["html_table"]=html_mars_profile
    mars_scrape["table"]=mars_table

    #scrape mars hemispheres site
    url_mars_hemispheres="https://marshemispheres.com/"
    browser.visit(url_mars_hemispheres)
    html_mars_hemispheres=browser.html
    soup_mars_hemispheres=bs(html_mars_hemispheres,'html.parser')

    #create list for hemisphere image url's
    hemisphere_image_urls=[]

    #scrape Cerberus hemisphere
    url_cerberus="https://marshemispheres.com/cerberus.html"
    browser.visit(url_cerberus)
    html_cerberus=browser.html
    soup_cerberus=bs(html_cerberus,'html.parser')
    img_results=soup_cerberus.find_all("div",class_="downloads")
    for img_result in img_results:
        img_path=img_result.a['href']
        img_url_cerberus=f"https://marshemispheres.com/{img_path}"

    title_results=soup_cerberus.find_all("div",class_="cover")
    for title_result in title_results:
        title_cerberus=title_result.find('h2',class_='title').text
        title_cerberus=title_cerberus.replace('Enhanced','')
        title_cerberus=title_cerberus.strip()

    cerebus={}
    cerebus["title"]=title_cerberus
    cerebus["img_url"]=img_url_cerberus
    hemisphere_image_urls.append(cerebus)
    
    #scrape Schiaparelli hemisphere
    url_schiaparelli="https://marshemispheres.com/schiaparelli.html"
    browser.visit(url_schiaparelli)
    html_schiaparelli=browser.html
    soup_schiaparelli=bs(html_schiaparelli,'html.parser')
    img_results=soup_schiaparelli.find_all("div",class_="downloads")
    for img_result in img_results:
        img_path=img_result.a['href']
        img_url_schiaparelli=f"https://marshemispheres.com/{img_path}"

    title_results=soup_schiaparelli.find_all("div",class_="cover")
    for title_result in title_results:
        title_schiaparelli=title_result.find('h2',class_='title').text
        title_schiaparelli=title_schiaparelli.replace('Enhanced','')
        title_schiaparelli=title_schiaparelli.strip()

    schiaparelli={}
    schiaparelli["title"]=title_schiaparelli
    schiaparelli["img_url"]=img_url_schiaparelli
    hemisphere_image_urls.append(schiaparelli)

    #scrape Syrtis Major hemisphere
    url_syrtis="https://marshemispheres.com/syrtis.html"
    browser.visit(url_syrtis)
    html_syrtis=browser.html
    soup_syrtis=bs(html_syrtis,'html.parser')

    img_results=soup_syrtis.find_all("div",class_="downloads")
    for img_result in img_results:
        img_path=img_result.a['href']
        img_url_syrtis=f"https://marshemispheres.com/{img_path}"

    title_results=soup_syrtis.find_all("div",class_="cover")
    for title_result in title_results:
        title_syrtis=title_result.find('h2',class_='title').text
        title_syrtis=title_syrtis.replace('Enhanced','')
        title_syrtis=title_syrtis.strip()

    syrtis={}
    syrtis["title"]=title_syrtis
    syrtis["img_url"]=img_url_syrtis
    hemisphere_image_urls.append(syrtis)

    #scrape Valles Marineris hemisphere
    url_valles="https://marshemispheres.com/valles.html"
    browser.visit(url_valles)
    html_valles=browser.html
    soup_valles=bs(html_valles,'html.parser')

    img_results=soup_valles.find_all("div",class_="downloads")
    for img_result in img_results:
        img_path=img_result.a['href']
        img_url_valles=f"https://marshemispheres.com/{img_path}"

    title_results=soup_valles.find_all("div",class_="cover")
    for title_result in title_results:
        title_valles=title_result.find('h2',class_='title').text
        title_valles=title_valles.replace('Enhanced','')
        title_valles=title_valles.strip()

    valles={}
    valles["title"]=title_valles
    valles["img_url"]=img_url_valles
    hemisphere_image_urls.append(valles)

    #update scrape dictionary
    mars_scrape["hemispheres"]=hemisphere_image_urls

    browser.quit() 
    return mars_scrape