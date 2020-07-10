import requests, os
from lxml import html
from utils import get_page, get_page_identifier, get_url_from_identifier, delay

# don't do this recursively due to max recursion depth after collecting for a while
# instead, we will use a while loop
def scrape(url):
    while url is not None:
        # sometimes, requests loads a malformed page
        # we know all pages exist with PNG data, next url, etc
        # keep retrying until we get it
        while True:
            try:
                page = get_page(url)
                id = get_page_identifier(url)
                save_poem(page, id)
                url = next_page_url(page)
                print(url)
                delay()
            except Exception as error:
                print('Failure at volume {}, issue {}, page {}: {}'.format(id['volume'], id['issue'], id['page'], error))

# we save the poems in a directory called PNGs
def save_poem(page, id):
    # each page has a scanned image representing the poem
    images = page.xpath('//img/@src')
    candidate_images = [i for i in images if i.startswith('https://static.poetryfoundation.org/jstor/')]
    if len(candidate_images) == 0:
        raise RuntimeError('Failure: No image found for volume {}, issue {}, page {}'.format(id['volume'], id['issue'], id['page']))
    elif len(candidate_images) > 1:
        raise RuntimeError('Failure: Too many images found for volume {}, issue {}, page {}'.format(id['volume'], id['issue'], id['page']))
    else:
        print('Saved volume {}, issue {}, page {}'.format(id['volume'], id['issue'], id['page']))
        with open(os.path.join('PNGs', '{}_{}_{}.png').format(id['volume'], id['issue'], id['page']), 'wb') as f:
            f.write(requests.get(candidate_images[0]).content)


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

# starting_url = 'https://www.poetryfoundation.org/poetrymagazine/browse?volume=1&issue=1&page=1'
# last page is get_url_from_identifier({'volume' : 193, 'issue' : 3, 'page' : 101})
starting_url = get_url_from_identifier({'volume' : 135, 'issue' : 2, 'page' : 5})
scrape(starting_url)
