from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH: Path = Path(__file__).parent.parent
CHROME_DRIVER_NAME = 'chromedriver'
CHROME_DRIVER_PATH: Path = ROOT_PATH / 'bin' / CHROME_DRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROME_DRIVER_PATH)  # flake8: noqa
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('http://youtube.com')
    sleep(5)
    browser.quit()