import os, requests
from lxml import html, etree
from utils import get_page, get_page_identifier, get_url_from_identifier, delay
from functools import reduce

# this time, instead of paginating, let's use the files in PNGs (run scrape_pngs.py before scrape_metada)
# these scripts were built separately because I didn't know we needed the metadata at first
# Since we don't know the functionality of metadata or pagination before starting,
# it seems helpful to keep the files separate from cognitive load and fault tolerance perspectives

def filename_to_url(filename):
    f_nums = [int(i) for i in filename.split('_')]
    return get_url_from_identifier({'volume': f_nums[0], 'issue': f_nums[1], 'page': f_nums[2]})

def strip_ending(filename):
    return filename.split('.')[0]

def name_score(name):
    return reduce(lambda acc, next: acc * 1000 + int(next), name.split('_'), 1)

def remaining_urls():
    png_filenames = map(strip_ending, os.listdir('PNGs'))
    metadata_filenames = map(strip_ending, os.listdir('Metadata'))
    remaining_filenames = sorted(set(png_filenames) - set(metadata_filenames), key=name_score)
    return list(map(filename_to_url, remaining_filenames))

def capture_metadata(page):
    class_to_grab = 'c-assetStack-auxiliary'
    metadata_elements = page.xpath('//div[contains(@class, \'{}\')]'.format(class_to_grab))
    return str([etree.tostring(i) for i in metadata_elements])

def save_captured_data(metadata, id):
    with open(os.path.join('Metadata', '{}_{}_{}.txt').format(id['volume'], id['issue'], id['page']), 'w') as f:
        f.write(metadata)

def scrape():
    for url in remaining_urls():
        try:
            id = get_page_identifier(url)
            page = get_page(url)
            metadata_to_save = capture_metadata(page)
            save_captured_data(metadata_to_save, id)
            print('Saved volume {}, issue {}, page {} - {:.2f}% finished'.format(id['volume'], id['issue'], id['page'], 100 * len(os.listdir('Metadata')) / len(os.listdir('PNGs'))))
        except Exception as error:
            print('Failure at volume {}, issue {}, page {}: {}'.format(id['volume'], id['issue'], id['page'], error))
            print('Skipping for now')

scrape()
