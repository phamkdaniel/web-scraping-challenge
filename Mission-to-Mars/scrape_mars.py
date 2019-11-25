#!/usr/bin/env python
# coding: utf-8

import pandas as pd

import requests
from bs4 import BeautifulSoup

from splinter import Browser


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_latest_news():
    """ scrapes NASA for latest news on mars
    """
    # get news titles and text
    mars_news_url = 'https://mars.nasa.gov/news/'

    news_soup = get_soup(mars_news_url)

    news_title_div = news_soup.find('div', {'class':'content_title'})
    news_desc_div = news_soup.find('div', {'class':'rollover_description_inner'})

    news_title = news_title_div.text.strip()
    news_p = news_desc_div.text.strip()

    return news_title, news_p

def get_feature_image():
    """ get url for featured image from the Jet Propulsion Laboratory website
    """
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    with Browser(headless=True) as b:
        b.visit(jpl_url)

        carousel = b.find_by_css('div[class="carousel_items"]').first
        carousel.find_by_css('a').first.click()

        img = b.find_by_css('img[class="fancybox-image"]').first
        featured_image_url = img['src']

    return featured_image_url

def get_mars_facts():
    """ get table of facts about mars
    """
    mars_facts_url = 'https://space-facts.com/mars/'
    facts_soup = get_soup(mars_facts_url)

    # gets mars facts table
    facts_table = facts_soup.find('table', {'class':'tablepress'})

    col1_data = facts_table.find_all('td', {'class':'column-1'})
    col2_data = facts_table.find_all('td', {'class':'column-2'})

    col1 = [td.text for td in col1_data]
    col2 = [td.text for td in col2_data]

    facts_table_df = pd.DataFrame({'description':col1, 'value':col2}).set_index('description')

    return facts_table_df.to_html(classes="table table-striped")

def get_mars_weather():
    """ get weather data from first tweet from mars twitter page
    """
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'

    twitter_soup = get_soup(mars_twitter_url)

    first_tweet_p = twitter_soup.find('p', {'class':'TweetTextSize'})

    mars_weather = first_tweet_p.text.replace('\n', ', ').split('pic')[0]

    return mars_weather

def get_hemisphere_urls():
    """ gets images of hemispheres from astrogeology
    """
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_image_urls = []

    with Browser(headless=True) as b:
        b.visit(mars_hemisphere_url)

        div_item = b.find_by_css('div[class="item"]')

        enhanced_img_links = []
        title_list = []
        for item in div_item:
            enhanced_img_links.append(item.find_by_css('a')['href'])
            title_list.append(item.find_by_css('h3').text.rsplit(' ', 1)[0])

        img_url_list = []
        for link in enhanced_img_links:
            b.visit(link)

            wide_img = b.find_by_css('img[class="wide-image"]')
            src = wide_img['src']

            img_url_list.append(src)

    for i in range(len(title_list)):
        hemisphere_image_urls.append(
            {
                'title' : title_list[i],
                'img_url': img_url_list[i]
            }
        )

    return hemisphere_image_urls


def scrape():
    news_title, news_p = get_latest_news() 

    mars_data = {
        'latest_news' : {'title':news_title, 'par':news_p},
        'feat_img' : get_feature_image(),
        'facts_table_html' : get_mars_facts(),
        'mars_weather' : get_mars_weather(),
        'hemisphere_imgs' : get_hemisphere_urls()
    }

    return mars_data
