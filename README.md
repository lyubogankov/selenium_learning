## Checking out Selenium!

### Motivation
My goal with this project was to learn the basics of Selenium to programmatically control a webbrowser (in my case, Google Chrome using chromedriver).

I had two potential usecases in mind:
- Automating extraction of transaction data from my bank account and credit card websites
- Automating data pull for a project at work

### Project Description
A friend found this [Danish IQ test](http://mensa.dk/iqtest/index.html) and shared it with our Discord server.

I noticed that the test didn't randomize the questions - it was always the same questions every time!

I wrote this script to learn Selenium basics and also to see if I could figure out the answers to every question and maximize my score!

**Note** I needed to [download a specific version of the Chrome chromedriver](https://chromedriver.chromium.org/downloads) for use with my version of Google Chrome!  To run this project, you will need to download the chromedriver that matches your own version of Chrome.

**Strategy**
Finding the answers to each question requires multiple iterations.

- During the first iteration, answer `A` for each of the 39 questions.  Note the IQ score presented at the end.
- Then, focus on each question individually:
    - Try each possible answer not yet tried (`B` -> `H`).
    - Observe the score at the end of the test.
        - If the score stays the same as when we answered `A`, that means neither `A` nor the letter submitted on the current iteration are correct.
        - If the score increases relative to when we answered `A`, that means we found the right answer and are done with this question (no need to look at remaining answers, if any).  It can take up to 7 additional iterations to find the right answer, if `H` is the correct answer.
        - If the score decreases relative to when we answered `A`, that means `A` was actually the correct answer and we are done with this question.  This occurs when we pick `B`, so it doesn't take too long.
- Once we know the correct answer for each question, we can enter them all and get the high score!

### Use for finances automation
I was excited to use Selenium for scraping my bank and credit card websites, but grew wary when reading about how [websites may attempt to detect usage of Selenium](https://old.reddit.com/r/Python/comments/ov73ci/selenium_with_python_security/h78emig/) (or specific webdriver implementations) to prevent bots.  I decided not to risk it with my financial services websites, as I do not want my accounts closed.  So use of Selenium for this project was unfortunately off of the table.

### Use at work
My manager expressed concern at me using a Python module that could control the web browser.  I looked through the Python library's imports to verify that nothing malicious was present.
- [Python script to find all import statements from the Selenium module](deps.py)
- [LibreOffice .ods spreadsheet with my "verdicts" for each import (whether it posed a risk)](deps.ods)

This approach does nothing to guarantee the safety of the chromedriver code, however.  I found the [source code](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/chrome/test/chromedriver/) but did not analyze it like I did the Python Selenium code.