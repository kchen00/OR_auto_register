import requests
import csv
import json
from bs4 import BeautifulSoup

# Create a session
session = requests.Session()

login_payload = {
    "txtUsername": "YOURMATRICID",
    "txtPassword": "YOURPASSWORD",
    "commit": ""
}

subject_to_take = {}
failed_register = {}

# reading the csv files to register
with open("subject_to_take.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        subject_to_take[row["subject_code"]] = {
            "sem": int(row["sem"]),
            "subject_code": row["subject_code"],
            "lect_group": row["lect_group"],
            "tut_group": row["tut_group"],
            "repeat_subj": ""
        }

# Create a session
session = requests.Session()

# method to print out the dictionary in json format
def print_json(input):
    # Convert the dictionary to a JSON string
    json_str = json.dumps(input, indent=4)
    # Print the JSON string
    print(json_str)

# method to write response.text as html files
def write_html(file_name, response):
    with open(file_name, "w") as f:
        f.write(response.text)
        f.close()

# pre testing the input to make sure it is correct and working properly
def test():
    print_json(subject_to_take)

    # login into OR system
    login_page_url = "https://or.ump.edu.my/or/LoginCheck.jsp"
    #logging into the or 
    login = session.post(login_page_url, data=login_payload)
    write_html("login_test.html", login)
    
    # navigation test 
    sem_1_url = "https://or.ump.edu.my/or/main.jsp?action=CurrentSemester"
    sem_1 = session.get(sem_1_url)
    write_html("sem_1_page.html", sem_1)

    sem_2_url = "https://or.ump.edu.my/or/main.jsp?action=NextSemester"
    sem_2 = session.get(sem_2_url)
    write_html("sem_2_page.html", sem_2)


def register():
    # login into OR system
    login_page_url = "https://or.ump.edu.my/or/LoginCheck.jsp"
    #logging into the or 
    login = session.post(login_page_url, data=login_payload)

    # url for page
    sem_1_url = "https://or.ump.edu.my/or/main.jsp?action=CurrentSemester"
    sem_1_register_url = "https://or.ump.edu.my/or/CurrentSemester/action/add_subject.jsp"
    sem_2_url = "https://or.ump.edu.my/or/main.jsp?action=NextSemester"
    sem_2_register_url = "https://or.ump.edu.my/or/NextSemester/action/add_subject.jsp"

    for subject in subject_to_take:    
        payload = {
            "subject_code": subject_to_take[subject]["subject_code"],
            "lect_group": subject_to_take[subject]["lect_group"],
            "tut_group": subject_to_take[subject]["tut_group"],
            "repeat_subj": ""
        }

        # check which sem is the subject
        if subject_to_take[subject]["sem"] == 1:
            session.get(sem_1_url)
            register = session.post(sem_1_register_url, data=payload)
        elif subject_to_take[subject]["sem"] == 2:
            session.get(sem_2_url)
            register = session.post(sem_2_register_url, data=payload)

        # extracting the error message when register failed
        soup = BeautifulSoup(register.content, 'html.parser')
        # Find the <div> element with class 'alert alert-info'
        div_element = soup.find('div', class_='alert alert-info')
        # Extract the text within the <div> element
        div_text = div_element.get_text()
        # Print the extracted text
        print(div_text)

        # check if the error is due to section full already
        if "The section/group is already full" in div_text:
            failed_register[subject_to_take[subject]["subject_code"]] = payload

# uncomment register() to run the code
test()
# register()
print_json(failed_register)

# Clear cookies and session-related data
session.cookies.clear()
# Close the session to end the session
session.close()
