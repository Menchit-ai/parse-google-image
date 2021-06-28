from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import urllib
import sys
import time
from bs4 import BeautifulSoup
import requests

from PIL import Image
import io
import base64
from random import randint
from math import floor
from selenium.common.exceptions import ElementNotInteractableException
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("query", help="type which word(s) you want to search on google image",type=str)
parser.add_argument("number", help="how many images do you want to download",type=int)
parser.add_argument("-d", "--directory", default="./dataset",help="choose in which directory you want to store the images", type=str)
parser.add_argument("-v", "--verbose", default=0, help="0 for no output, 1 to print only the result, 2 for full output", type=int)
args = parser.parse_args()

# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
os.environ['MOZ_HEADLESS'] = '1'

# Configuration
download_path = args.directory+"/"
# Images
words_to_search = args.query
nb_to_download = args.number
v = args.verbose==1
full_v = args.verbose==2

def main():
    search_and_save(words_to_search,nb_to_download,download_path)

def scroll(driver):
    SCROLL_PAUSE_TIME = 2
   
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def load_page(driver, nb_scroll):
    for i in range(nb_scroll):
        scroll(driver)
        try:
            show_more = driver.find_elements_by_class_name("mye4qd")
            show_more[0].click()
        except ElementNotInteractableException as e : return i
       
def download_elements(elements,text,number,driver):
    if len(elements) < number: number = len(elements)
    cpt = 0
    i = 0
    while(cpt < number):
        e = elements[i]
        e.click()
        try:
            image = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[4]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img")
            url = image.get_attribute("src")
            name = str(image.get_attribute("alt"))
            name = name.replace(" ","_")
            name = "".join([character for character in name if character.isalnum()])
       
            cpt += download_url(url,text+"/"+name,cpt)
        except Exception as e:
            if full_v : print(e)
        i += 1
        if i==len(elements): return cpt
    return cpt
               
def download_url(url,text,_id):
    filename = download_path+text+".jpg"
    try:
        img_data = requests.get(url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
        if full_v : print(os.path.basename(filename) + " downloaded !")
        return 1
    except Exception as e:
        if full_v : print(e)
        elif v : print("Cant download",os.path.basename(filename))
        return 0
               
               
def search_and_save(text, number,download_path):
    # Number_of_scrolls * 400 images will be opened in the browser
    number_of_scrolls = floor(number/ 400) +1
    if full_v : print("Search : "+text+" ; number : "+str(number)+" ; scrolls : "+str(number_of_scrolls))

    # Connect to Google Image
    url = "https://www.google.co.in/search?q="+text+"&source=lnms&tbm=isch"
    driver = webdriver.Firefox()
    driver.get(url)
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    extensions = {"jpg", "jpeg", "png", "gif"}
       
    load_page(driver,number_of_scrolls)
    if full_v : print("\nPage loaded")

    print("Starting download")
    download_path = download_path.replace(" ", "_")
    text = text.replace(" ", "_")
    # Create directories to save images
    if not os.path.exists(download_path):
            os.makedirs(download_path)

    if not os.path.exists(download_path + text):
        os.makedirs(download_path + text)

   
    elements = driver.find_elements_by_xpath("//img[@class='rg_i Q4LuWd']")
    downloaded = download_elements(elements,text,number,driver)
    driver.quit()

    if v : print("Total downloaded : "+ str(downloaded)+ "/"+ str(number)+"\n")

if __name__ == "__main__":
    main()