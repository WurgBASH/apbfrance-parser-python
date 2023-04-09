#!/usr/bin/env python3

from typing import List
from json import load, dump
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from telegram import Bot

from config import config, logger, PROJ_ROOT
from model.Car import Car


def get_new_events(url: str = 'http://apbfrance.com/catalog/all?lang=pl&display=list') -> List[Car]:

    try:
        with open(PROJ_ROOT / 'dataset/refs.json', encoding='utf-8') as file:
            dataset = load(file)
    except:
        dataset = {}

    stored_refs = dataset["refs"] if "refs" in dataset else []

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    second_driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    second_driver.maximize_window()

    cars = []

    try:
        driver.get(url=url)

        tables = driver.find_elements(
            by=By.CSS_SELECTOR, value='div.vehicle_list > table > tbody')

        manufacturers = driver.find_elements(
            by=By.CSS_SELECTOR, value='div#content > h2')

        for table_index, table in enumerate(tables):
            try:
                rows = table.find_elements(by=By.CSS_SELECTOR, value='tr')
                manufacturer = manufacturers[table_index].text

                for row in rows:
                    cols = row.find_elements(by=By.CSS_SELECTOR, value='td')
                    link = cols[0].find_element(
                        by=By.CSS_SELECTOR, value='a').get_attribute('href')

                    data = [col.text for col in cols]
                    data.pop()

                    car = Car(manufacturer, *data, link)
                    cars.append(car)

            except Exception as e:
                logger.error(f"{e}. Line: {e.__traceback__.tb_lineno}")

    except Exception as e:
        logger.error(f"{e}. Line: {e.__traceback__.tb_lineno}")

    refs = [car.ref for car in cars]

    diff = list(set(refs) - set(stored_refs))

    for new_car in [car for car in cars if car.ref in diff]:
        Bot(config['TOKEN']).send_message(chat_id=int(config['GROUP_ID']),
                                          text=str(new_car), disable_web_page_preview=True)
        sleep(0.2)

    with open(PROJ_ROOT / 'dataset/refs.json', 'w', encoding='utf-8') as file:
        dump({"refs": refs}, file, indent=2, ensure_ascii=False)

    return cars


if __name__ == '__main__':
    logger.info('Starting script...')
    get_new_events()
