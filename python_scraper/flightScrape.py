from operator import itemgetter
from time import sleep, strftime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

PATH = "/Users/bilalosman/Desktop/SideStuff"
driver = webdriver.Chrome(executable_path=PATH + '/chromedriver')

def get_best_link(dp_place, arr_place, start_date, end_date):
    link = ('https://www.kayak.com/flights/' + dp_place+ '-' + arr_place +
            '/' + start_date + '-flexible-3days/' + end_date + '-flexible-3days?sort=bestflight_a')
    driver.get(link)

def get_cheap_link(dp_place, arr_place, start_date, end_date):
    link = ('https://www.kayak.com/flights/' + dp_place+ '-' + arr_place +
            '/' + start_date + '-flexible-3days/' + end_date + '-flexible-3days?sort=price_a')
    driver.get(link)

def get_quick_link(dp_place, arr_place, start_date, end_date):
    link = ('https://www.kayak.com/flights/' + dp_place+ '-' + arr_place +
            '/' + start_date + '-flexible-3days/' + end_date + '-flexible-3days?sort=duration_a')
    driver.get(link)

def close_popup(): #if popup occurs
        try:
            xp_popup_close = '//button[contains(@id,"dialog-close") and contains(@class,"Button-No-Standard-Style close ")]'
            driver.find_element(by=By.XPATH, value=xp_popup_close).click()
        except Exception as e:
            pass

def load_again():
    try:
        more_searches = '//a[@class = "moreButton"]'
        driver.find_element(by=By.XPATH, value=more_searches).click()
    except Exception as e:
        print('button not pressed')
        pass

def flightScrape():
    #first the flight times, durations, and destinations
    staleEle = True
    xp_sections = '//*[@class="section duration allow-multi-modal-icons"]'
    while(staleEle):
        try:
            flight_locs =[val.text for val in driver.find_elements(by=By.XPATH, value=xp_sections)]
            staleEle = False
        except Exception as e:
            staleEle = True
    flight_dep = flight_locs[::2]
    flight_arr = flight_locs[1::2]
    if not flight_dep or not flight_arr:
        raise SystemExit
    # print(flight_dep)
    # print(flight_arr)
    duration_dp, duration_arr, dp_loc_name, arr_loc_name = ([] for _ in range(4))

    for flight in flight_dep:
        hold, *route = flight.split('\n')
        duration_dp.append(hold)
        dp_loc_name.append(''.join(route)) 
    for flight in flight_arr:
        hold, *route = flight.split('\n')
        duration_arr.append(hold)
        arr_loc_name.append(''.join(route))

    #next the stops
    staleEle = True
    while(staleEle):
        try:
            stops = [val.text[0].replace('n', '0') for val in driver.find_elements(by=By.XPATH, value= '//div[@class="section stops"]/div[1]')]
            staleEle = False
        except Exception as e:
            staleEle = True
    
    stops_dp, stops_arr = stops[::2], stops[1::2]
    staleEle = True
    while(staleEle):
        try:
            stop_cities = [val.text for val in driver.find_elements(by=By.XPATH, value= '//div[@class="section stops"]/div[2]')]
            staleEle = False
        except Exception as e:
            staleEle = True
    stop_names_dp, stop_names_arr = stop_cities[::2], stop_cities[1::2]

    #next the dates of the flights
    xp_dates = '//div[@class="section date"]'
    staleEle = True
    while(staleEle):
        try:
            get_dates = [val.text for val in driver.find_elements(by=By.XPATH, value=xp_dates)]
            staleEle = False
        except Exception as e:
            staleEle = True
    date_dp, date_arr = get_dates[::2], get_dates[1::2]
    date_dp, date_arr = [d.split() for d in date_dp], [d.split() for d in date_arr]

    day_dp, day_arr = list(map(itemgetter(0), date_dp)), list(map(itemgetter(0), date_arr))
    weekday_dp, weekday_arr = list(map(itemgetter(1), date_dp)), list(map(itemgetter(1), date_arr))

    #next the prices
    xp_price = '//a[@class="booking-link "]/span[@class="price option-text"]/span[@class = "price-text"]'
    xp_pricesub = '//a[@class="booking-link whisky-booking-link "]/span[@class="price option-text"]/span[@class = "price-text"]'

    staleEle = True
    while(staleEle):
        try:
            staleEle = False
            pricesN = driver.find_elements(by=By.XPATH, value=xp_price)
            priceN_list = [price.text for price in pricesN if price.text != '']
        except Exception as e:
            staleEle = True
    
    staleEle = True
    while(staleEle):
        try:
            staleEle = False
            prices_sub = driver.find_elements(by=By.XPATH, value=xp_pricesub)
            prices_sub_list = [prices_sub.text for prices_sub in prices_sub if prices_sub.text != '']
        except Exception as e:
            staleEle = True


    # other stuff like airline company
    staleEle = True
    schedules = driver.find_elements(by=By.XPATH, value='//div[@class="section times"]')
    airlines = []
    while(staleEle):
        try:
            staleEle = False
            for schedule in schedules:
                temp, airline = schedule.text.split('\n')
                airlines.append(airline)
        except Exception as e:
            staleEle = True
    
    airline_dp, airline_arr = airlines[::2], airlines[1::2]

    #an issue with specific airlines. This is the fix
    # print(airline_dp)
    # print(priceN_list)
    # print(prices_sub_list)
    subair = ['Alaska Airlines', 'Virgin Atlantic', 'Iberia', 'British Airways']
    n, s = 0, 0
    if(len(prices_sub_list) == 0):
        prices_list = priceN_list
    else:
        prices_list = []
        for i in range(len(airline_dp)):
            if(airline_dp[i] in subair):
                prices_list.append(prices_sub_list[s])
                s+=1
            else:
                prices_list.append(priceN_list[n])
                n+=1

    # print(duration_dp, duration_arr, dp_loc_name, arr_loc_name)
    # print(date_dp, date_arr)
    # print(stops_dp, stops_arr, stop_names_dp, stop_names_arr)
    # print(day_dp, day_arr, weekday_dp, weekday_arr )
    # print(prices_list)
    # print(hours_dp, hours_arr, airline_dp, airline_arr)

    flight_base = {
        'TO NAME': dp_loc_name,
        'TO DURATION': duration_dp,
        'TO DATE': day_dp,
        'TO WEEKDAY': weekday_dp,
        'TO STOPS': stops_dp,
        'TO STOP NAMES': stop_names_dp,
        'TO AIRLINE': airline_dp,
        'FROM NAME': arr_loc_name,
        'FROM DURATION': duration_arr,
        'FROM DATE': day_arr,
        'FROM WEEKDAY': weekday_arr,
        'FROM STOPS': stops_arr,
        'FROM STOP NAMES': stop_names_arr,
        'FROM AIRLINE': airline_arr,
        'PRICE': prices_list
    }
    # print(flight_base)
    # print(len(dp_loc_name), len(duration_dp), len(day_dp), len(weekday_dp), len(stops_dp), len(stop_names_dp),
    #         len(airline_dp), len(arr_loc_name), len(duration_arr), len(day_arr), len(weekday_arr), len(stops_arr),
    #         len(stop_names_arr), len(airline_arr), len(prices_list))
    try:
        data_flights = pd.DataFrame(data=flight_base)
    except Exception as e:
        print('Error in scraping. Please try again later.')
        return None
    data_flights['timestamp'] = strftime("%Y%m%d-%H%M") 
    return data_flights















    

    



