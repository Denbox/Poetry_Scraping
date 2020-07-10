import requests, time
from lxml import html

# the site is not entirely inconsistent. Luckily, October 1912 to December 2008 uses a simple format.
# basically, we start at the url for October 1912, and keep hitting the right arrow button through December 2008.

def get_page(url):
    # download page and save the html data
    page_data = requests.get(url).content
    # parse html as a tree to make it searchable
    page_as_tree = html.fromstring(page_data)
    return page_as_tree

# extract volume, issue, and page numbers from url
def get_page_identifier(url):
    id = dict([i.split('=') for i in url.split('?')[1].split('&')])
    return id

def get_url_from_identifier(id):
    return 'https://www.poetryfoundation.org/poetrymagazine/browse?volume={}&issue={}&page={}'.format(id['volume'], id['issue'], id['page'])

# VERY IMPORTANT! When webscraping, always make sure to not flood the servers with requests
# It is possible to use a bunch of threads and scrape the entire site very quickly
# Instead, the little scraper patiently goes through one by one
def delay():
    time.sleep(1)
