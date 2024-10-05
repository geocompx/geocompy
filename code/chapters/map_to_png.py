import folium
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
def map_to_png(m, fname, path=None):
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.set_window_size(1008, 612)
    if not path:
        path = os.getcwd()
    # save the map, open with selenium, wait for initial load
    m.save('{}/map.html'.format(path))
    browser.get('file://{}/map.html'.format(path))
    time.sleep(5)
    browser.save_screenshot('images/{}.png'.format(fname))
    browser.quit()