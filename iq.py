# imports recommended by 'Getting Started' docs.
# https://selenium-python.readthedocs.io/getting-started.html
from selenium import webdriver
from collections import defaultdict
from time import sleep
from pprint import pprint

'''
# for inputting key-presses
from selenium.webdriver.commons.keys import Keys

# for mouse-clicks
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
'''

# Attempting to make a ContextManager so I can use 'with'
#   https://book.pythontips.com/en/latest/context_managers.html
class AutomatedWebpage(object):
	def __init__(self, url):
		self.driver = webdriver.Chrome('/home/lyubo/script/selenium/chromedriver_v97')
		self.driver.get(url)
	def __enter__(self):
		return self.driver
	def __exit__(self, type, value, traceback):
		self.driver.close()

def random_attempt():	
	import random
	with AutomatedWebpage('http://mensa.dk/iqtest/index.html') as driver:
		# get a reference to all of the test options (a-h) as local variables
		options = [chr(i) for i in range(97, 105)]
		for letter in options:
			exec(f'''{letter} = driver.find_element_by_xpath("//div[@class='col-xs-6 col-sm-4 col-md-3']/div[@class='center']/span[text()='{letter.upper()}']/parent::*/img")''')
		# take the test - select options!
		choices = dict()
		for i in range(1, 40):
			choice = chr(random.randrange(97, 105))
			exec(f"{choice}.click()")
			choices[i] = choice
		# click through to the Resultat page
		driver.find_elements_by_class_name('finish')[0].click()
		driver.find_elements_by_class_name('finish')[1].click()
		# interpret the results and store!
		test_results = driver.find_element_by_xpath("//p[@class='notetext'][1]/u[2]").text
	print(test_results)
	print(choices)


def iterative_attempt(target_question, target_letter):	
	with AutomatedWebpage('http://mensa.dk/iqtest/index.html') as driver:
		# get a reference to all of the test options (a-h) as local variables
		options = [chr(i) for i in range(97, 105)]
		for letter in options:
			exec(f'''{letter} = driver.find_element_by_xpath("//div[@class='col-xs-6 col-sm-4 col-md-3']/div[@class='center']/span[text()='{letter.upper()}']/parent::*/img")''')
		# take the test - select options!
		for i in range(1, 40):
			if i == target_question:
				exec(f"{target_letter}.click()")
			else:
				exec(f"a.click()")
		# click through to the Resultat page
		driver.find_elements_by_class_name('finish')[0].click()
		driver.find_elements_by_class_name('finish')[1].click()
		# interpret the results and return!
		test_results = driver.find_element_by_xpath("//p[@class='notetext'][1]/u[2]").text

	if "mindre end" in test_results:
		return 78  # one lower than lowest that is naturally returned?.
		# test_results = test_results[-2:] # 79
	return int(test_results)

def obtain_best_score(answerdict):	
	with AutomatedWebpage('http://mensa.dk/iqtest/index.html') as driver:
		# get a reference to all of the test options (a-h) as local variables
		options = [chr(i) for i in range(97, 105)]
		for letter in options:
			exec(f'''{letter} = driver.find_element_by_xpath("//div[@class='col-xs-6 col-sm-4 col-md-3']/div[@class='center']/span[text()='{letter.upper()}']/parent::*/img")''')
		# take the test - select options!
		for answer in answerdict.values():
			exec(f"{answer}.click()")
		# click through to the Resultat page
		driver.find_elements_by_class_name('finish')[0].click()
		driver.find_elements_by_class_name('finish')[1].click()
		# interpret the results and return!
		test_results = driver.find_element_by_xpath("//p[@class='notetext'][1]/u[2]").text
	return test_results

def solve_iq_test():
	baseline_score = iterative_attempt(-1, '')
	answerdict = {i:''  for i in range(1,40)}
	for question in range(1, 40):
		print(f'Optimizing #{question}')
		#		       b - h
		for i in range(98, 105):
			letter = chr(i)
			score = iterative_attempt(question, letter)
			print(f"\t...tried answering [{letter.upper()}, got {score:>3}]")
			# this means that the baseline_score is already highest ('a' is right answer)
			if score < baseline_score:
				answerdict[question] = 'a'
				break
			# this means that 'a' was the wrong answer, and we just found the correct one!
			elif score > baseline_score:
				answerdict[question] = letter
				break

	best_score = obtain_best_score(answerdict)
	print('-'*100)
	print(f"The best score possible is: {best_score}")
	pprint(answerdict)

if __name__ == "__main__":
	solve_iq_test()
	#random_attempt()

'''
setup:
	driver = webdriver.Chrome()
	driver.get("{url}")


locating/differentiating between the 8 choices:
	driver.find_elements_by_xpath("//div[@class='col-xs-6 col-sm-4 col-md-3']/div[@class='center']/span[text()='A']")
		I can iterate over the 8 choices by changing the text I search for (A-H).

		This apparently uses xpath, which is a W3C standard.  Fancy that!
		https://www.w3schools.com/xml/xpath_intro.asp

	However -- this only points me at the <span> containing the text.  The clickable part of this document is the image!
	Thankfully, xpath allows us to go up the HTML tree to a parent, and then down to the image sibling, which contains the 
	click-listener that responds and gives the answer.

	elem = driver.find_element_by_xpath("//div[@class='col-xs-6 col-sm-4 col-md-3']/div[@class='center']/span[text()='C']/parent::*/img")
	elem.click()
		I can pre-define the options A-H, and just reuse them.  Good to know!
		Caveat - they need to be defined for each single attempt at the IQ test.


Interacting with the test to finish and obtain / parse the score:
	Test page:
		finish = driver.find_element_by_class_name('finish')
		finish.click()
	Next info page:
		finish = driver.find_elements_by_class_name('finish')
		finish[1].click()


Parsing the results from the Resultat page:
	{element}.text gets the text from the current element.


Retaking the test
	Just open it again!


IQ test:  http://mensa.dk/iqtest/index.html




Misc
	button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "{name}")))
		unnecessary, but cool!  Apparently this tool can wait until a button becomes clickable, that's necessary for some webpages.


Tab save
	https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
	https://selenium-python.readthedocs.io/navigating.html
	https://selenium-python.readthedocs.io/locating-elements.html
	https://selenium-python.readthedocs.io/waits.html

	https://towardsdatascience.com/most-people-screw-up-multiple-percent-changes-heres-how-to-do-get-them-right-b86bd6ef4b72
'''
