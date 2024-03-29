#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:36:46 2019

@author: Tawanda
"""
import sys
import argparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


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
        browser.get('https://www.oursky.com/')
        button = browser.find_element_by_class_name('btn-header')
        button.click()
        print('=======Button Click test was successful=======')
    except NoSuchElementException as ex:
        print(f'Error :: No such element : {ex}')