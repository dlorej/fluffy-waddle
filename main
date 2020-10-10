from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key
from pynput.keyboard import Controller as Keyboard_control
import random
from datetime import datetime,timedelta
import pickle
import os

keyboard = Keyboard_control()

def main(username,password): # some component of scheduler, random time,skip days occasionally

     #copied from somewhere
    def get_text_excluding_children(driver, element):
        return driver.execute_script("""
        var parent = arguments[0];
        var child = parent.firstChild;
        var ret = "";
        while(child) {
            if (child.nodeType === Node.TEXT_NODE)
                ret += child.textContent;
            child = child.nextSibling;
        }
        return ret;
        """, element)

    class unique_follower():
        def __init__(self, username_id, follow_status, last_check_date):
            self.username = username_id
            self.follow_status = follow_status
            self.last_check_date = last_check_date


    random_interval = timedelta(hours=random.randint(4, 5), minutes=random.randint(0, 59),
                                seconds=random.randint(0, 59))

    browser = webdriver.Firefox()
    browser.implicitly_wait(5)
    browser.get('https://www.instagram.com/')

    #navigate into followers tab
    username_input,password_input = browser.find_elements_by_class_name('_2hvTZ.pexuQ.zyHYP')[0],browser.find_elements_by_class_name('_2hvTZ.pexuQ.zyHYP')[1]
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button = browser.find_element_by_class_name('Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB')
    login_button.click()
    not_now_1 = browser.find_element_by_class_name('sqdOP.yWX7d.y3zKF')# not_now_1 = browser.find_element_by_partial_link_text('Not Now')
    not_now_1.click()
    not_now_2 = browser.find_element_by_class_name('aOOlW.HoLwm')
    not_now_2.click()
    go_to_profile = browser.find_element_by_class_name('gmFkV')
    go_to_profile.click()
    save_profile_url = browser.current_url


    def check_followers(max_expected = 0):
        followers = browser.find_element_by_partial_link_text('followers')
        print(followers.get_attribute('class'))
        entire_followers = followers.find_element_by_class_name('g47SY')
        if max_expected == 0:
            num = get_text_excluding_children(browser, entire_followers)
            num = num.replace(',','')
            expected = int(num)
        else:
            expected = max_expected
        # num = ''.join([char for char in get_text_excluding_children(browser,followers) if char.isdigit()])
        followers.click()
        sleep(3)

        #click on followers tab to enable scrolling
        scroll = browser.find_element_by_class_name('isgrP')
        print('found')
        scroll.click()
        for i in range(40):
            keyboard.press(Key.page_down)
            sleep(0.05)
        follower_boxes_class_id = 'uu6c_'
        list_follower_boxes = browser.find_elements_by_class_name(follower_boxes_class_id)
        num_follower_boxes = len(list_follower_boxes)

        #scroll until the end
        while num_follower_boxes < expected:
            for i in range(40):
                keyboard.press(Key.page_down)
                sleep(0.05)
            list_follower_boxes = browser.find_elements_by_class_name(follower_boxes_class_id)
            num_follower_boxes = len(list_follower_boxes)

        # check instagram for followers
        latest_check_followers = []
        for index, follower_box in enumerate(list_follower_boxes):
            # full_path = 't2ksc.enpQJ.d7ByH.Jv7Aj.mArmR.MqpiF.FPmhX.notranslate._0imsa'
            name = follower_box.find_element_by_class_name('FPmhX.notranslate._0imsa')
            name_text = get_text_excluding_children(browser, name)
            if name_text == username:
                #change to dynamic
                continue
            #follow status
            button = follower_box.find_element_by_class_name('sqdOP.L3NKy')
            button_text = get_text_excluding_children(browser, button)
            new = unique_follower(name_text, button_text, str(datetime.now()))
            latest_check_followers.append(new)

        return latest_check_followers

    latest_check_followers = check_followers()



    #check txt file for followers
    last_check_followers = []
    with open('last_action_date.txt','r') as read_ladfile:
        if os.stat('last_action_date.txt').st_size == 0:
            print('Not running')
            first_time = True
        else:
            print('False')
            first_time = False
        ladfile_contents = read_ladfile.readlines()
        for line in ladfile_contents:
            username_id, follow_status, year, time = line.split(' ')
            last_check_date = year + ' ' + time.strip()
            new = unique_follower(username_id, follow_status, last_check_date)
            last_check_followers.append(new)

    for i in last_check_followers:
        print(vars(i))

    if first_time == False:
        #check own followers
        picking = []
        max_added = 10
        for index,uf in enumerate(last_check_followers):
            uf_lcd = datetime.strptime(uf.last_check_date,'%Y-%m-%d %H:%M:%S.%f')
            #wait 1 day before adding again
            if uf_lcd + timedelta(days = 1) < datetime.now():
                if uf.follow_status == 'Following':
                    picking.append(index)
        first_loop = True
        #number of people to check follower list
        while max_added > 0:
            print('max added '+str(max_added))
            if first_loop != True:
                #change this
                browser.get(save_profile_url)
                sleep(3)
                followers = browser.find_element_by_partial_link_text('followers')
                followers.click()
                sleep(3)
            random_person = random.choice(picking)
            print('this is the person whose list im looking at: ' + last_check_followers[random_person].username)
            last_check_followers[random_person].last_check_date = str(datetime.now())
            picking.remove(random_person)
            selected_person = browser.find_element_by_partial_link_text(latest_check_followers[random_person].username)
            selected_person.click()
            print('checking')
            sp_followers_list = check_followers()
            print('done')
            num_gonna_follow = random.randint(1,min(5,len(sp_followers_list)))
            print('num gonna follow ' + str(num_gonna_follow))
            ngf_save_value = num_gonna_follow
            for followers_of_sp in sp_followers_list:
                print('check 1')
                if followers_of_sp.follow_status == 'Follow':
                    print('check 2, added')
                    child = browser.find_element_by_partial_link_text(followers_of_sp.username)
                    parentx6 = child.find_element_by_xpath('../../../../..')
                    button = parentx6.find_element_by_class_name('sqdOP.L3NKy')
                    button.click()
                    num_gonna_follow -= 1
                    if num_gonna_follow < 1:
                        break
                    sleep(1)
            max_added -= ngf_save_value
            first_loop = False

    with open('last_action_date.txt', 'w') as ladfile:
        for uf2 in latest_check_followers:
            for index,uf in enumerate(last_check_followers):
                if uf2.username == uf.username:
                    break
                if index + 1 == len(last_check_followers):
                    ladfile.write(uf2.username + ' ' + uf2.follow_status + ' ' + uf2.last_check_date + '\n')
        for uf in last_check_followers:
            ladfile.write(uf.username + ' ' + uf.follow_status + ' ' + uf.last_check_date + '\n')

main()
