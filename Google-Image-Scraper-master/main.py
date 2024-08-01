# # -*- coding: utf-8 -*-
# """
# Created on Sun Jul 12 11:02:06 2020
#
# @author: OHyic
#
# """
# #Import libraries
# from GoogleImageScrapper import GoogleImageScraper
# import os
# from typing import Tuple
#
# #Define file path
# webdriver_path = os.path.normpath(os.getcwd()+"\\webdriver\\chromedriver.exe")
# image_path = os.path.normpath(os.getcwd()+"\\photos")
#
# # search_keys is what images you want to search e.g ['fish'] would download fish images
# # number_of_images is the number of images you will attempt to download
# # headless is a bool for headless
# # It does not download images other than jpg and png so it may not always be the same number of images
# # min_resolution and max_resolution is the max and min resolution of images downloaded
# # If its too high, it will lag
# def run_scrapy(search_keys: list, number_of_images: int, min_resolution: Tuple[int,int],
#                max_resolution: Tuple[int, int], image_path):
#     #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
#     # search_keys= ["food", "tree"]
#
#     #Parameters
#     # number_of_images = 20
#     # min_resolution=(0,0)
#     # max_resolution=(1000,1000)
#
#     #Main program
#     for search_key in search_keys:
#         image_scrapper = GoogleImageScraper(webdriver_path,image_path,search_key,number_of_images,False,min_resolution,max_resolution)
#         image_urls = image_scrapper.find_image_urls()
#         image_scrapper.save_images(image_urls)
