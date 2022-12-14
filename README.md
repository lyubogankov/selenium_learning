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

- During the first iteration, answer `A` for each of the 39 questions.  Note the IQ score presented at the end (79).
- Then, focus on each question individually:
    - Try each possible answer not yet tried (`B` -> `H`).
    - Observe the score at the end of the test.
        - If the score stays the same as when we answered `A` (79), that means neither `A` nor the letter submitted on the current iteration are correct.
        - If the score increases relative to when we answered `A` (81), that means we found the right answer and are done with this question (no need to look at remaining answers, if any).  It can take up to 7 additional iterations to find the right answer, if `H` is the correct answer.
        - If the score decreases relative to when we answered `A` (78), that means `A` was actually the correct answer and we are done with this question.  This occurs when we pick `B`, so it doesn't take too long.
- Once we know the correct answer for each question, we can enter them all and get the high score, 141!


<details>
<summary><b>Answers (spoiler warning)</b></summary>

    1: 'c',
    2: 'f',
    3: 'g',
    4: 'c',
    5: 'b',
    6: 'h',
    7: 'f',
    8: 'a',
    9: 'h',
    10: 'c',
    11: 'c',
    12: 'h',
    13: 'e',
    14: 'g',
    15: 'd',
    16: 'b',
    17: 'f',
    18: 'e',
    19: 'b',
    20: 'c',
    21: 'a',
    22: 'e',
    23: 'e',
    24: 'c',
    25: 'f',
    26: 'd',
    27: 'd',
    28: 'd',
    29: 'b',
    30: 'e',
    31: 'd',
    32: 'a',
    33: 'b',
    34: 'a',
    35: 'c',
    36: 'a',
    37: 'f',
    38: 'a',
    39: 'f'
    
</details>

### Use for finances automation
I was excited to use Selenium for scraping my bank and credit card websites, but grew wary when reading about how [websites may attempt to detect usage of Selenium](https://old.reddit.com/r/Python/comments/ov73ci/selenium_with_python_security/h78emig/) (or specific webdriver implementations) to prevent bots.  I decided not to risk it with my financial services websites, as I do not want my accounts closed.  Use of Selenium for this project was unfortunately off of the table.

### Use at work
My manager expressed concern at me using a Python module that could control the web browser.  I looked through the Python library's imports to verify that nothing malicious was present.
- Python script to find all import statements from the Selenium module ([deps.py](deps.py))
- LibreOffice .ods spreadsheet with my "verdicts" for each import (whether it posed a risk) ([deps.ods](deps.ods))

This approach does nothing to guarantee the safety of the chromedriver code, however.  I found the [source code](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/chrome/test/chromedriver/) but did not analyze it like I did the Python Selenium code.