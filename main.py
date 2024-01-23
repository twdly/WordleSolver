from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

def main():
    validWords = get_valid_words()
    driver = setup_driver()
    open_wordle(driver)
    wordGuessed = False
    guessNumber = 1
    wordToGuess = ""

    while (not wordGuessed and guessNumber < 7):
        wordToGuess = select_word(validWords)
        try_word(driver, wordToGuess)
        wordGuessed = get_guess_result(driver, guessNumber)
        validWords = filter_word_list(validWords)
        guessNumber += 1

    if wordGuessed:
        print(f"The word is {wordToGuess}")
    else:
        print("Cringe has been posted")
    

def setup_driver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    driver.implicitly_wait(10)
    return driver

def open_wordle(driver):
    driver.find_element(By.CLASS_NAME, "Welcome-module_button__ZG0Zh").click()
    driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb").click()
    time.sleep(3)

def try_word(driver, word):
    actions = ActionChains(driver)
    actions.send_keys(word)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(3)

def get_valid_words():
    wordFile = open("words.txt", "r")
    wordsAsString = wordFile.read()
    wordsAsString = wordsAsString.replace('"', '').replace(',', '')
    return wordsAsString.split(' ')
    
def select_word(validWords):
    return validWords[random.randrange(len(validWords))]

def get_guess_result(driver, rowNumber):
    row = driver.find_elements(By.XPATH, f"//div[@aria-label='Row {rowNumber}']/*/*")
    for letter in row:
        if letter.accessible_name.find("absent") >= 0 or letter.accessible_name.find("present in another position") >= 0:
            return False
    return True

def filter_word_list(validWords):
    return validWords

if __name__ == "__main__":
    main()
