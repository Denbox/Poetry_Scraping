import os, requests
from lxml import html
from scrape_pngs import get_page, get_page_identifier, get_url_from_identifier, delay

# this time, instead of paginating, let's use the files in PNGs (run scrape_pngs.py before scrape_metada)
# these scripts were built separately because I didn't know we needed the metadata at first
# Since we don't know the functionality of metadata or pagination before starting,
# it seems helpful to keep the files separate from cognitive load and fault tolerance perspectives

# we will save our metadata in a Metadata directory. Recall that the PNGs are in the PNGs directory.
def remaining_urls():
    png_ids = 
    collected_ids = None
    return ids
