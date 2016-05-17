#!/usr/bin/python3
import argparse
import re
import os
import threading
import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# --------------------------------------
#    Web page displayer
#
#    ToDo:  - show different webpages in a browser
#           - Read the config file once every 10 minutes
#           - Have different sets that are displayed on different times of the day.
#               - On the morning
#               - In the afternoon
#
# --------------------------------------
# Argument parser
parser = argparse.ArgumentParser(description='Start a browser and display pages.')
parser.add_argument('-t', dest='timeinterval', help='Time to show each page')
#parser.add_argument('-o', dest='html_log_file_name', help='Output in html format. With no filetype given')
#parser.add_argument('-d', dest='html_log_file_dir', help='Output folder for the result')
# parser.add_argument('-s', dest='show_all', help='Show all lines')


config_file_name = 'browser-shed.conf'
time_to_run = 5.0        # Run for 5 minutes in then re-read the config
#-----------------
# Url lists
url_list = []

#-----------------
# Classes


#class MyThread (threading.Thread):
#    def __init__(self, threadID, trace_file, html_name, out_dir):
#        threading.Thread.__init__(self)
#        self.threadID = threadID
#        self.trace_file = trace_file
#        self.html_name = html_name
#        self.out_dir = out_dir
#    def run(self):
#        #print ('Do action {0} with name {1} to output {2}'.format(self.trace_file, self.html_name, self.out_dir))
#        parse_file( self.trace_file, self.html_name, self.out_dir)
#        #print ('Exiting ' + self.trace_file )
#        url_result = self.out_dir + '/' + self.html_name + '.html'
#        webbrowser.open(url_result)


def get_config_path():
    """ Try to find where the config files are. Using env variable PATH """
    env_path = os.environ['PATH']
    env_parts = env_path.split(':')
    for dir in env_parts:
        if os.path.isfile(dir + '/' + config_file_name):
            return dir + '/'
    return ''


def read_url_list(url_conf_list):
    """ Read the url config list. """

    config_path = get_config_path()

    try:
        url_config_file    = open(config_path + config_file_name)
        for conf_line in url_config_file:
            tmp_conf = conf_line.rstrip()
            #parts = tmp_conf.split(';',2)
            #add_row = BoxCalcConf(parts[0],parts[1])
            url_conf_list.append(tmp_conf)
        url_config_file.close()
    except IOError:
        print ("Error: can\'t find file or read data " + config_file_name)
        raise


def test_firefox():
    browser = webdriver.Firefox()
    #print(browser)
    browser.get('https://wiki.rd.consafe1.org/wiki/index.php/Main_Page')
    time.sleep(float( args.timeinterval)) # delays
    browser.get('https://www.google.com')


def test_chrome():
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    #driver = webdriver.Chrome('/usr/bin/chromedriver')  # Optional argument, if not specified will search path.
    driver.get('http://www.google.com/xhtml');
    time.sleep(5) # Let the user actually see something!
    search_box = driver.find_element_by_name('q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5) # Let the user actually see something!
    driver.quit()

def display_urls(b_driver, url_list, show_time):
    """ Read the url config list. """

    # Go for 5 minutes
    t_end = time.time() + 60 * time_to_run
    while time.time() < t_end:
        for url in url_list:

            b_driver.get(url);
            time.sleep(float(show_time))



#----------------------
#  Main starts
#----------------------

args = parser.parse_args()

print('Time laps = ' + str(args.timeinterval))
if args.timeinterval == 0:
    args.timeinterval = 10

read_url_list(url_list)

print (url_list)

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
#driver = webdriver.Chrome('/usr/bin/chromedriver')  # Optional argument, if not specified will search path.

driver.get('http://www.google.com/xhtml');
time.sleep(1) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys( Keys.F11)

time.sleep(10) # Let the user actually see something!

display_urls(driver, url_list, args.timeinterval)

driver.quit()

#test_chrome()

exit(0)