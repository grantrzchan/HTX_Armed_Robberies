import pdb
import os
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from halo import Halo

#function for file download:
def download_file(url, file_path):
    res = requests.get(url, stream=True)
    #download file by chunks, chunk size 1024 bytes
    with open(file_path,'wb') as file:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return

def get_excel_urls(hrefs):
    href_list = [x.get_attribute('href') for x in hrefs]
    dl_list = [item for item in href_list if item.find('xls') != -1]
    return dl_list

def get_excel_data(dl_list):
    for item in dl_list:
        item_name = item[item.find('xls/')+len('xls/') ::]
        download_file(item, '.\\temp\\' + item_name)
    return

#delete temp folder if exists
if os.path.isdir('.\\temp'):
    shutil.rmtree('.\\temp')

#make temp directory
os.mkdir('.\\temp')


chrome_options =  webdriver.ChromeOptions()
#suppress unnecessary logs from chrome driver
chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])
#enable headless browsing
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

spinner = Halo(text='Initializing Chrome Driver', spinner='line')
spinner.start()

#navigate to website
driver.get('https://www.houstontx.gov/police/cs/Monthly_Crime_Data_by_Street_and_Police_Beat.htm')
#explicit wait for page to fully load
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#collect all excel files via <a> tags
hrefs = driver.find_elements_by_xpath('//a[@href]')
dl_list = get_excel_urls(hrefs)
get_excel_data(dl_list)
spinner.succeed()
spinner.start('Downloading files')

#navigate to website archive
driver.get('https://www.houstontx.gov/police/cs/crime-stats-archives.htm')
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#collect all excel files via <a> tags
hrefs = driver.find_elements_by_xpath('//a[@href]')
dl_list = get_excel_urls(hrefs)
get_excel_data(dl_list)
spinner.succeed('Download completed')

#terminate web scraper
driver.quit()
spinner.stop()
