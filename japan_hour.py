#open chrome
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#use mouse and keyboard
from pynput.mouse import Button
from pynput.mouse import Controller as Mouse_control
from pynput.keyboard import Key
from pynput.keyboard import Controller as Keyboard_control

#copy from clipboard
from tkinter import Tk

#using ffmpeg and youtube-dl with cmd line
import subprocess

#wait for site to load
import time

#delete files
import os

#control mouse and keyboard
mouse = Mouse_control()
keyboard = Keyboard_control()

#list of locations
network_tab = (1660,126)
first_result = (1400,355)
copy = (1450,450)
copy_link = (1640,455)
search_bar = (1380,180)


def open_chrome(path = r'C:\Users\User\Downloads\Internet download\chromedriver_win32\chromedriver.exe'):
    #input if location of path changes
    #return driver

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")
##    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    return driver

def open_site(driver,site_url = r'https://www.channelnewsasia.com/news/video-on-demand/japanhour'):
    driver.get(site_url)

def play_video(driver,tries = 15,element_name = 'video__custom-duration'):
    try:
        link = driver.find_element_by_class_name(element_name)
        link.click()
    except Exception:
        tries -= 1
        if tries == 0:
            quit()
        else:
            time.sleep(2)
            return play_video(driver,tries,element_name)

def open_network_tab():
    keyboard.press(Key.shift_l)
    keyboard.press(Key.ctrl_l)
    keyboard.press('j')
    keyboard.release(Key.shift_l)
    keyboard.release(Key.ctrl_l)
    keyboard.release('j')
    time.sleep(2)
    keyboard.press(Key.shift_l)
    keyboard.press(Key.ctrl_l)
    keyboard.press('p')
    keyboard.release(Key.shift_l)
    keyboard.release(Key.ctrl_l)
    keyboard.release('p')
    time.sleep(2)
    keyboard_type('show network')
    time.sleep(1)
    keyboard.press(Key.enter)
##    mouse.position = network_tab
##    time.sleep(2)
##    mouse.click(Button.left)
##    time.sleep(2)

def search_network(search_term,tries = 15):
    time.sleep(2)
    subprocess.call('echo off | clip', shell=True)
    keyboard_type(search_term)
    time.sleep(2)

    #get first result
    mouse.position = first_result

    #copy link
    mouse.click(Button.right)
    mouse.position = copy
    time.sleep(0.5)
    mouse.move(25,5)
    mouse.click(Button.left)
    time.sleep(0.5)
    mouse.position = (copy_link[0],copy_link[1])
    time.sleep(0.5)
    mouse.click(Button.left)

    if Tk().clipboard_get() == '' and tries > 0:
        tries -= 1
        time.sleep(2)
        return search_network(search_term,tries)
    else:
        return Tk().clipboard_get()

def keyboard_type(word):
    for char in word:
        keyboard.press(char)
        keyboard.release(char)

def clear_search():
    mouse.position = search_bar
    time.sleep(2)
    mouse.click(Button.left)
    mouse.click(Button.left)
    mouse.click(Button.left)
    time.sleep(1)
    keyboard.press(Key.backspace)

def get_title(driver,element_name = 'video__custom-subtitle'):
    try:
        title = driver.find_element_by_class_name(element_name)
    except exceptions.NoSuchElementException:
        quit()
    temp = title.text
    temp = temp.replace('-',' ')
    temp = temp.replace('/','')
    temp = temp.replace(r"'",'')
    while '  ' in temp:
        temp = temp.replace('  ',' ')
    temp = temp.replace(' ', '_')
    print(temp)
    return temp

def download_link(link,title):
    file_location = r'C:\Users\User\Desktop\ffmpeg-20200426-1128aa8-win64-static\bin'
    if link.endswith(r'en.vtt'):
        working_file = r'C:\Users\User\Videos\Japan_Hour\working/'
        file_name = working_file + title + '_subtitle.vtt'
        num = 1
        while os.path.exists(file_name):
            file_name = working_file + title + '_' + str(num) + '_subtitle.vtt'
            num += 1
        print(file_name)
        command = 'youtube-dl ' + link + ' -o ' + file_name
        subprocess.call(command,cwd = file_location,shell = True)
        print(command)
        file_name = change_subtitle_format(file_name)
    elif link.endswith(r'(format=m3u8-aapl)'):
        working_file = r'C:\Users\User\Videos\Japan_Hour/'
        temp_file_name = r'C:\Users\User\Videos\Japan_Hour/' + title + '.mp4'
        num = 1
        while os.path.exists(temp_file_name):
            temp_file_name = r'C:\Users\User\Videos\Japan_Hour/' + title + '_' + str(num) + '.mp4'
            num += 1
        file_name = temp_file_name.replace('.mp4','_temp.mp4')
        print(file_name)
        command = 'youtube-dl ' + link + r' -o ' + temp_file_name
        print(command)
        subprocess.call(command, cwd=file_location, shell=True)
    return file_name

def change_subtitle_format(subtitle_file_name):
    file_location = r'C:\Users\User\Desktop\ffmpeg-20200426-1128aa8-win64-static\bin'
    command = 'ffmpeg -i ' + subtitle_file_name + ' ' + subtitle_file_name[:-3] + 'ass'
    print(command)
    subprocess.call(command,cwd = file_location,shell = True)
    os.remove(subtitle_file_name)
    return subtitle_file_name[:-3] + 'ass'

def merge_video(video_file_name,subtitle_file_name):
    file_location = r'C:\Users\User\Desktop\ffmpeg-20200426-1128aa8-win64-static\bin'
    new_name = video_file_name.replace('_temp','')
    subtitle_file_name = subtitle_file_name.replace(':','\\:')
    command = 'ffmpeg -i ' + video_file_name + ' -vf \"ass=\'' + subtitle_file_name + '\'\" ' + new_name
    command = command.replace('/','\\')
    print(command)
    subprocess.call(command,cwd = file_location,shell = True)
    os.remove(video_file_name)

def main_jh():
    driver = open_chrome()
    open_site(driver)
    open_network_tab()
    video_link = search_network(r'manifest(format=')
    title = get_title(driver)
    play_video(driver)
    clear_search()
    subtitle_link = search_network(r'en.vtt',30)
    video_file = download_link(video_link,title)
    subtitle_file = download_link(subtitle_link,title)
    driver.quit()
    merge_video(video_file,subtitle_file)

main_jh()
