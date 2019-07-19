#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:44:47 2019

@author: tawanda
"""
import sys
import time
import pandas
import argparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


BASE_URL = 'https://azure.microsoft.com/en-us/pricing/calculator/?&OCID=AID2000113_SEM_iaxXnj2c&MarinID=iaxXnj2c_334925916936_azure%20calculator_e_c__67435449310_aud-390212648291:kwd-44260433768&lnkd=Google_Azure_Brand&dclid=CM_g0JGOvuMCFYrO3god5gIH1Q'
NOTHERN_EUROPE = 'europe-north'
LINUX = 'linux'
WINDOWS = 'windows'
ONLY = 'os-only'
STANDARD = 'standard'


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--driver", help="path to chrome driver")
    args = parser.parse_args()
    
    if not args.driver:
        print("Please enter a valid path to the chrome driver ( --driver argument )")
        sys.exit(1)
    
    browser = webdriver.Chrome(executable_path=args.driver)
    browser.implicitly_wait(10)
    browser.maximize_window()
    
    try:
        browser.get(BASE_URL)
        products_tab_elements = browser.find_elements_by_xpath('//button[@title="Virtual Machines"]')
#        print(f'length of elements = {len(elements)}')
        
        virtual_machines_button = products_tab_elements[0]
        virtual_machines_button.click()
        
        time.sleep(5) # TODO replace with Wait func
        
        saved_estimates_tab =  browser.find_elements_by_id('estimates-picker')[0]
        saved_estimates_tab.click()
        
        
        input_tag = browser.find_elements_by_xpath('//input[@value ="one-year"]')[0]
        input_tag.click()
        
        # Set drop downs
        region_tag = browser.find_element_by_xpath(f"//option[@value='{NOTHERN_EUROPE}']")
        region_tag.click()
        
        os_tag = browser.find_element_by_xpath(f"//option[@value='{WINDOWS}']")
        os_tag.click()
        
        type_tag = browser.find_element_by_xpath(f"//option[@value='{ONLY}']")
        type_tag.click()
        
        tier_tag = browser.find_element_by_xpath(f"//option[@value='{STANDARD}']")
        tier_tag.click()
    
        # Get all instance name values
        all_instances = []
        
        instance_list_elements =  browser.find_elements_by_xpath('//*[@id="size"]/option')
        for element in instance_list_elements:
            element.click()
            price = browser.find_elements_by_xpath("//span[@class='numeric']/span")[0].text
            
            instance = {}
            instance["Region"] = NOTHERN_EUROPE
            instance["OS"] = WINDOWS
            instance["Type"] = ONLY
            instance["Tier"] = STANDARD
            instance["Name"] = element.text.replace("Effective cost per month", "")
            instance["Price"] = price
            all_instances.append(instance)
        
        prices_df = pandas.DataFrame(all_instances)
        print(prices_df)
        prices_df.to_csv('prices.csv')
        
        print('=======Button Click test was successful=======')
    except NoSuchElementException as ex:
        print(f'Error :: No such element : {ex}')