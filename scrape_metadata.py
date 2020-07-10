import os, requests
from lxml import html
from utils import get_page, get_page_identifier, get_url_from_identifier, delay

# this time, instead of paginating, let's use the files in PNGs (run scrape_pngs.py before scrape_metada)
# these scripts were built separately because I didn't know we needed the metadata at first
# Since we don't know the functionality of metadata or pagination before starting,
# it seems helpful to keep the files separate from cognitive load and fault tolerance perspectives

def filename_to_url(filename):
    f_nums = [int(i) for i in filename.split('_')]
    return get_url_from_identifier({'volume': f_nums[0], 'issue': f_nums[1], 'page': f_nums[2]})

def strip_ending(filename):
    return filename.split('.')[0]

# we will save our metadata in a Metadata directory. Recall that the PNGs are in the PNGs directory.
def remaining_urls():
    png_filenames = map(strip_ending, os.listdir('PNGs'))
    metadata_filenames = map(strip_ending, os.listdir('Metadata'))
    remaining_filenames = set(png_filenames) - set(metadata_filenames)
    return list(map(filename_to_url, remaining_filenames))

def save_metadata(page):
    raise NotImplementedError

def scrape():
    for url in remaining_urls():
        try:
            print(url)
            id = get_page_identifier(url)
            page = get_page(url)
            save_metadata(page)
        except Exception as error:
            print('Failure at volume {}, issue {}, page {}: {}'.format(id['volume'], id['issue'], id['page'], error))
            print('Skipping for now')

scrape()
