import requests
import time
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

def save_poem(page, id):
    # each page has a scanned image representing the poem
    images = page.xpath('//img/@src')
    candidate_images = [i for i in images if i.startswith('https://static.poetryfoundation.org/jstor/')]
    if len(candidate_images) == 0:
        print('Failure: No image found for volume {}, issue {}, page {}'.format(id['volume'], id['issue'], id['page']))
    elif len(candidate_images) > 1:
        print('Failure: Too many images found for volume {}, issue {}, page {}'.format(id['volume'], id['issue'], id['page']))
    else:
        print('Saved volume {}, issue {}, page {}'.format(id['volume'], id['issue'], id['page']))
        with open('{}_{}_{}.png'.format(id['volume'], id['issue'], id['page']), 'wb') as f:
            f.write(requests.get(candidate_images[0]).content)

# VERY IMPORTANT! When webscraping, always make sure to not flood the servers with requests
# It is possible to use a bunch of threads and scrape the entire site very quickly
# Instead, the little scraper patiently goes through one by one
def delay():
    time.sleep(1)

# if the next page exists, return the url
# otherwise, return None
def next_page_url(page):
    # this xpath searches the page for a link (a) with rel=next set
    # rel=next is commonly used for site pagination
    links = page.xpath('//a[@rel="next"]/@href')
    if links == []:
        return None
    else:
        return links[0]

# don't do this recursively due to max recursion depth after collecting for a while
# instead, we will use a while loop
def scrape(url):
    while url is not None:
        page = get_page(url)
        id = get_page_identifier(url)
        save_poem(page, id)
        url = next_page_url(page)
        delay()

# starting_url = 'https://www.poetryfoundation.org/poetrymagazine/browse?volume=1&issue=1&page=1'
starting_url = 'https://www.poetryfoundation.org/poetrymagazine/browse?volume=5&issue=1&page=26'
scrape(starting_url)
