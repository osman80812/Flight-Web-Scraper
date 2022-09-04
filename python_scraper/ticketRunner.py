import flightScrape
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
from openpyxl import Workbook

class PyScraper:
    
    def __init__(self, start_city='MSP', end_city='ORL', start_date='2022-09-10', end_date='2022-09-20'):
        print('Hello, here you can search for your ticket in a csv file!')
        self.start_city = start_city if start_city else input('Choose your Origin\n')
        self.end_city = end_city if end_city else input('Choose your Destination\n')
        self.start_date = start_date if start_date else input(
            'Search around which departure date? Please use YYYY-MM-DD format only\n')
        self.end_date = end_date if end_date else input(
            'Search around which arrival date? Again, please use YYYY-MM-DD format only\n')
        self.ticketRunner()


    def ticketRunner(self):
        print('Running ticketRunner..')
        #best flights
        flightScrape.get_best_link(self.start_city, self.end_city, self.start_date, self.end_date)
        sleep(randint(8,10))
        flightScrape.close_popup()

        flightScrape.load_again()
        sleep(randint(15,20))
        print('1st site opened. Now Scraping..')
        fs_best = flightScrape.flightScrape()
        fs_best['sort'] = 'best'
        # print(fs_best)
        sleep(randint(20,30))

        #cheapest flights
        flightScrape.get_cheap_link(self.start_city, self.end_city, self.start_date, self.end_date)
        sleep(randint(8,10))
        flightScrape.close_popup()

        flightScrape.load_again()
        sleep(randint(15,20))
        print('2nd site opened. Now Scraping..')
        fs_cheap = flightScrape.flightScrape()
        fs_cheap['sort'] = 'cheap'
        # print(fs_cheap)
        sleep(randint(20,30))

        #quickest results
        flightScrape.get_quick_link(self.start_city, self.end_city, self.start_date, self.end_date)
        sleep(randint(8,10))
        flightScrape.close_popup()

        flightScrape.load_again()
        sleep(randint(15,20))
        print('3rd site opened. Now Scraping..')
        fs_quick = flightScrape.flightScrape()
        fs_quick['sort'] = 'quick'
        # print(fs_quick)
        sleep(randint(20,30))
        #close website
        flightScrape.driver.close()

        #saving onto an excel file
        print('Creating flight database..')
        fs_data = fs_cheap.append(fs_best).append(fs_quick)
        fs_data.to_excel('{}_flights_{}-{}_from_{}_to_{}.xlsx'.format(strftime("%Y%m%d-%H%M"),
                                                                       self.start_city, self.end_city, self.start_date, self.end_date), 
                                                                       index=False)
        

run = PyScraper()

