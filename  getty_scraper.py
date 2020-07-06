import requests
from bs4 import BeautifulSoup
import csv
import os
from tqdm import tqdm

def turnToSoup(url):
    res = requests.get(url)
    contents = res.text
    soup = BeautifulSoup(contents, 'lxml')
    
    return soup

def get_images(soup, image_urls):
    container = soup.find('div', class_='search-content__gallery-pager-wrapper').findAll('img')
    for i in container:
        try:
            if i['src'].endswith('='):
                image_urls.append(i['src'])
        except:
            pass
    return image_urls

def create_train_test_split(samJack_image_urls, lauFish_image_urls, test_size=0.2):
    print('\nSplitting up data into train/test split (test size=0.2)')
    samJack_train = samJack_image_urls[:len(samJack_image_urls) - round(len(samJack_image_urls)*test_size)]
    samJack_test = samJack_image_urls[len(samJack_image_urls) - round(len(samJack_image_urls)*test_size):]

    lauFish_train = lauFish_image_urls[:len(lauFish_image_urls) - round(len(lauFish_image_urls)*test_size)]
    lauFish_test = lauFish_image_urls[len(lauFish_image_urls) - round(len(lauFish_image_urls)*test_size):]


    return samJack_train, samJack_test, lauFish_train, lauFish_test


def create_train_and_test_dirs():
    cwd = os.getcwd()
    print('Cheking if train directory exists ...')

    if os.path.exists(f'{cwd}/train'):
        print('Train directory already exists')
    else:
        print('Creating train directory')
        os.mkdir(f'{cwd}/train')
        os.mkdir(f'{cwd}/train/samuelJackson')
        os.mkdir(f'{cwd}/train/laurenceFishburne')

    print('\nCheking if test directory exists ...')
    if os.path.exists(f'{cwd}/test'):
        print('Test directory already exists\n')
    else:
        print('Creating test directory')
        os.mkdir(f'{cwd}/test')
        os.mkdir(f'{cwd}/test/samuelJackson')
        os.mkdir(f'{cwd}/test/laurenceFishburne')


def writeImagesToFile(samJack_train, samJack_test, lauFish_train, lauFish_test,samJack_image_urls,lauFish_image_urls):
    # Write images to directory 
    cwd = os.getcwd()

    print("\nWriting images to directory ... ")
    for index, image in enumerate(tqdm(samJack_train)):
        with open(f'{cwd}/train/samuelJackson/samJack_{index+1}.jpg', 'wb') as f:
            f.write(requests.get(image).content)
    
    print('Finished writing images of Samuel L Jackson to train.\n')
    for index, image in enumerate(tqdm(samJack_test)):
        with open(f'{cwd}/test/samuelJackson/samJack_{len(samJack_image_urls)-index}.jpg', 'wb') as f:
            f.write(requests.get(image).content)
    print('Finished writing images of Samuel L Jackson to test.\n')


    for index, image in enumerate(tqdm(lauFish_train)):
        with open(f'{cwd}/train/laurenceFishburne/lauFish_{index+1}.jpg', 'wb') as f:
            f.write(requests.get(image).content)
    print('Finished writing images of Laurence Fishburne to train.\n')


    for index, image in enumerate(tqdm(lauFish_test)):
        with open(f'{cwd}/test/laurenceFishburne/lauFish_{len(lauFish_image_urls)-index}.jpg', 'wb') as f:
            f.write(requests.get(image).content)
    print('Finished writing images of Laurence Fishburne to test.\n')

    
    print("Finished writing all images.")



def main():

    # get images for samuel jackson
    samJack_image_urls = []
    
    print('Searching for images...\n')
    for i in tqdm(range(1, 15)): # specify how many pages you want to scrape
        url = f'https://www.gettyimages.co.uk/photos/samuel-l-jackson?family=editorial&numberofpeople=one&page={i}&phrase=samuel%20l%20jackson&sort=mostpopular'
        soup = turnToSoup(url)
        samJack_image_urls = get_images(soup, samJack_image_urls)
    
    print(f'Found: {len(samJack_image_urls)} images of Samuel L Jackson\n')
    # get images for lau fishbourne
    lauFish_image_urls = []
    for i in tqdm(range(1, 15)):
        url = f'https://www.gettyimages.co.uk/photos/laurence-fishburne?family=editorial&numberofpeople=one&page={i}&phrase=laurence%20fishburne&sort=mostpopular'
        soup = turnToSoup(url)
        lauFish_image_urls = get_images(soup, lauFish_image_urls)
    
    print(f'Found: {len(lauFish_image_urls)} images of Laurence Fishburne\n')
    samJack_train, samJack_test, lauFish_train, lauFish_test = create_train_test_split(samJack_image_urls, lauFish_image_urls, test_size=0.2)
    create_train_and_test_dirs()
    writeImagesToFile(samJack_train, samJack_test, lauFish_train, lauFish_test,samJack_image_urls,lauFish_image_urls)

main()