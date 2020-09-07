from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

keys = ' engineer'
page = 0

file = open('company.txt')
done_file = open('done.txt','r')
donelist = done_file.readlines()
done_file.close()

#keyword = raw_input('input your keyword ')
#page = raw_input('start from which page? ')

drive = webdriver.Firefox()
wait = WebDriverWait(drive,10)


drive.get('https://www.linkedin.com/uas/login')
email = drive.find_element_by_id('session_key-login')
email.send_keys('12315dyd@gmail.com')
password = drive.find_element_by_id('session_password-login')
password.send_keys('******')
password.send_keys(Keys.RETURN)

#time.sleep(5)

for keyword in file.readlines():
    if keyword in donelist:
        continue
    time.sleep(5)
    select = Select(drive.find_element_by_id('main-search-category'))
    select.select_by_visible_text('People')

    drive.find_element_by_id('main-search-box').clear()
    search = drive.find_element_by_id('main-search-box')
    keyword = keyword[:-1]
    search.send_keys(keyword+keys)
    search.send_keys(Keys.RETURN)


    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'search-results')))
    except:
        continue
    if 10>=int(page) > 1:
        link = drive.find_element_by_link_text(page).get_attribute('href')
        drive.get(link)

    for i in range(5):
        time.sleep(3)
        section = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'search-results')))
        #section = drive.find_element_by_class_name('search-results')
        list = section.find_elements_by_class_name('people')
        for people in list:
          try:
            name = people.find_element_by_class_name('main-headline').text
            if "LinkedIn Member" is not name:
              print name
            else:
              continue
            try:
              button = people.find_element_by_class_name('primary-action-button')
              if button.text == 'Connect':
                button.click()

            except:
              pass
          except:
            if 'invite New Connection' in drive.title:
              drive.back()


        time.sleep(2)

        try:
            nextpage = drive.find_element_by_link_text('Next >').get_attribute('href')
        except:
            break

        drive.get(nextpage)
    done=open('done.txt','a')
    done.writelines(keyword+'\n')

    done.close()
drive.close()
