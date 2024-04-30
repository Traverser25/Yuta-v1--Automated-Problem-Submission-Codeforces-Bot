import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment this line to run the browser in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# Set up the WebDriver
driver = webdriver.Chrome(options=chrome_options)


def get_submission_id(url, driver):
    driver.get(url)
    driver.execute_script("document.getElementById('verdictName').value = 'OK';")
    driver.execute_script("document.getElementById('programTypeForInvoker').value = 'cpp.g++14';")
    driver.execute_script("document.querySelector('input[value=\"Apply\"]').click();")
    submission_id = driver.execute_script(
        "return document.querySelector('a.view-source').getAttribute('submissionid');"
    )
    time.sleep(0.5)
    return submission_id


def extract_num(string):
    match = re.match(r'^(\d+)', string)
    if match:
        return match.group(1)
    else:
        return None


def getproblems(url):
    links_with_codes = []

    # URL of the page
    # url =" https://codeforces.com/problemset/page/5?tags=800-800&order=BY_RATING_ASC"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links with href containing "/problemset/problem"
    problem_links = soup.find_all('a', href=lambda href: href and "/problemset/problem" in href)

    # Convert the links to the desired form and prepend "https://codeforces.com"
    for link in problem_links:
        original_link = link['href']
        # Extracting the number and problem code from the original link
        parts = original_link.split("/")
        number = parts[-2]
        problem_code = parts[-1]
        # Constructing the full link with the correct format
        full_link = f"https://codeforces.com/problemset/status/{number}/problem/{problem_code}"
        links_with_codes.append((full_link, number + problem_code))

    return links_with_codes


def get_accepted_submission(url, cd):
    try:
        submission_id = get_submission_id(url, driver)

        if submission_id:
            pf = str(extract_num(cd))
            submission_url = f"https://codeforces.com/problemset/submission/{pf}/{submission_id}"
            response = requests.get(submission_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            source_code_element = soup.find('pre', id='program-source-text')
            source_code = source_code_element.text.strip()
            return {"submission_id": submission_id, "source_code": source_code}

        else:
            return "No accepted submission found for C++ or Python."

    except Exception as e:
        return f"An error occurred: {e}"


# Example usage:  cnt=17

# You might need to specify the path to your webdriver executable
def delay(x):
    time.sleep(x)


def codeforces_login(driver, username, password):
    # Load the login page
    driver.get("https://codeforces.com/enter")

    # Wait for the username or email input field
    # Fill in the login form
    driver.execute_script(
        """
        document.getElementById('handleOrEmail').value = arguments[0];
        document.getElementById('password').value = arguments[1];
        document.getElementsByClassName('submit')[0].click();
        """,
        username,
        password
    )

    # Wait for the login process to complete
    time.sleep(5)

    # Check if login was successful
    if "Problemset | Codeforces" not in driver.title:
        print("Login failed.")
        return True
    else:
        print("Login successful.")
        return True


def submit_codeforces_solution(driver, language_value, problem_code, source_code):
    # Load the login page

    # Load the submission page
    driver.get("https://codeforces.com/problemset/submit")
    delay(1)

    # Select the language from the dropdown
    driver.execute_script("document.querySelector('select[name=\"programTypeId\"]').value = arguments[0];",
                          language_value)

    # Enter the problem code
    driver.execute_script("document.querySelector('input[name=\"submittedProblemCode\"]').value = arguments[0];",
                          problem_code)

    # Click the toggleEditorCheckbox to show the editor
    driver.execute_script("document.getElementById('toggleEditorCheckbox').click();")

    # Find the textarea element by its ID and make it visible
    driver.execute_script("document.getElementById('sourceCodeTextarea').style.display = 'block';")

    # Enter the source code into the textarea
    driver.execute_script("document.getElementById('sourceCodeTextarea').value = arguments[0];", source_code)

    # Click the submit button
    driver.execute_script("document.getElementById('singlePageSubmitButton').click();")
    time.sleep(0.5)


codeforces_login(driver, "Traverser_Steal69", "yutabot123")

for i in range(52,56):
    with open("logger.txt","a") as f:
        f.write("page : - "+str(i)+"\n")
    url = f"https://codeforces.com/problemset/page/{i}?order=BY_RATING_ASC"
    cnt = 0  # cur solved 366
    problem_links_with_codes = getproblems(url)
    start_time = time.time()
    for link, problem_code in problem_links_with_codes:
        if (cnt >0):
            pass

        if (cnt >=0):
            submission = get_accepted_submission(link, problem_code)
            try:
                # login_and_submit("I_steal69", "yutabot123", problem_code, submission["language"], submission["source_code"])
                submit_codeforces_solution(driver, "50", problem_code, submission["source_code"])

                print("Submission successful!")
                # time.sleep(0.5)
            except Exception as e:
                print(f"An error occurred: {e}")
        cnt += 1
        print(cnt)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    with open("logger.txt", "a") as f:
        f.write("took : "+str(execution_time)+" seconds\n")

#time at 76 18:43
#apply on page 5  after 35 problems ,same with pag 7  ,same with  8 ,full page 11,full page  15  ,half page 16 ,page 27 start from 60,full empty 28
#