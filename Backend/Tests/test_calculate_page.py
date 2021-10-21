import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select, By
import math
from time import sleep
import os
import datetime
os.environ['PATH'] += "C:\Program Files (x86)\Google\Chrome\Application"
# chrome_driver = webdriver.Chrome() 

def test_calculate_page():
    total_cash  = "1222"
    total_credit = "1000"
    chrome_driver = webdriver.Chrome()
    chrome_driver.get('http://localhost:3000/#/CalculateTips')
    chrome_driver.find_element_by_id("date_shift").send_keys("02/20/2020")
    chrome_driver.find_element_by_id("managers0").click()
    selected_shift_element = chrome_driver.find_element(By.NAME, 'shift')
    select_shift = Select(selected_shift_element)
    sleep(5)
    select_shift.select_by_value('evening')
    chrome_driver.find_element_by_id("Total-Cash").send_keys(total_cash)
    chrome_driver.find_element_by_id("Total-Credit").send_keys(total_credit)
    for i in range(0,3):
        chrome_driver.find_element_by_name("name"+str(i)).send_keys("Dvir"+str(i))
        chrome_driver.find_element_by_name("start_time"+str(i)).send_keys('10:24', 'AM')
        chrome_driver.find_element_by_name("finish_time"+str(i)).send_keys('12:00', 'PM')
        chrome_driver.find_element_by_name("total_time"+str(i)).send_keys("1"+str(i))
    chrome_driver.find_element_by_name("total_time4").send_keys("sentence")
    chrome_driver.find_element_by_name("Submit").click()

    # Check Results: 
    result = 0.0
    # try:
    sleep(20)
    total_tip_waiter = float(total_cash) + float(total_credit)

    for i in range(0,3):
        result += float(chrome_driver.find_element_by_name("total_tip_waiter"+str(i)).text)
    
    assert (math.ceil(result)) == total_tip_waiter, "Error occurrence in: " + str(result)
    print("Calculate Test Succes")
    chrome_driver.close()
         
