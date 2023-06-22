import requests
import csv
import json
from bs4 import BeautifulSoup
import time

# Create a session
session = requests.Session()

matric_id = None
password = None

# reading credential from files
with open("credential.txt", "r") as f:
    credentials = f.read()
    lines = credentials.split("\n")
    for line in lines:
        if line.startswith('MATRICID='):
            matric_id = line.split('=')[1].strip()
        elif line.startswith('PASSWORD='):
            password = line.split('=')[1].strip()

login_payload = {
    "txtUsername": matric_id,
    "txtPassword": password,
    "commit": ""
}

sem_1_register_url = "https://or.ump.edu.my/or/CurrentSemester/action/add_subject.jsp"
sem_2_register_url = "https://or.ump.edu.my/or/NextSemester/action/add_subject.jsp"

# url for page
register_url = [
    sem_1_register_url,
    sem_2_register_url
]

# reading the csv files to register
def read_subject_to_take():
    subject_to_take = {}
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
    return subject_to_take

# Create a session
session = requests.Session()

# method to print out the dictionary in json format
def print_json(input):
    # Convert the dictionary to a JSON string
    json_str = json.dumps(input, indent=4)
    # Print the JSON string
    print(json_str)

# a method to save subject that failed register as json
def save_json(failed_subject):
    with open('failed_subject.json', 'w') as file:
        json.dump(failed_subject, file)

# method to write response.text as html files
def write_html(file_name, response):
    with open(file_name, "w") as f:
        f.write(response.text)
        f.close()

# method to login
def login(credential):
    # login into OR system
    login_page_url = "https://or.ump.edu.my/or/LoginCheck.jsp"
    #logging into the or 
    login = session.post(login_page_url, data=credential)
    write_html("login_test.html", login)

    return login.status_code

def destroy_session():
    # Clear cookies and session-related data
    session.cookies.clear()
    # Close the session to end the session
    session.close()


def navigate_to_sem(sem):
    if sem == 1:
        # navigation test 
        sem_1_url = "https://or.ump.edu.my/or/main.jsp?action=CurrentSemester"
        sem_1 = session.get(sem_1_url)
        write_html("sem_1_page.html", sem_1)
        return sem_1.status_code

    elif sem == 2:
        sem_2_url = "https://or.ump.edu.my/or/main.jsp?action=NextSemester"
        sem_2 = session.get(sem_2_url)
        write_html("sem_2_page.html", sem_2)
        return sem_2.status_code

# pre testing the input to make sure it is correct and working properly
def test():
    subject_to_take = read_subject_to_take()
    print_json(subject_to_take)

    if login(login_payload) == 200:
        print("login is sucessful")
        if navigate_to_sem(1) == 200:
            print("navigation to sem 1 page is successful")
        else:
             print("navigation to sem 1 page failed")
        
        if navigate_to_sem(2) == 200:
            print("navigation to sem 2 page is successful")
        else:
             print("navigation to sem 2 page failed")
    else:
        print("Login failed, please check your matric id and password")

# a method to create payload
def create_payload(subject):
    payload = {
        "subject_code": subject["subject_code"],
        "lect_group": subject["lect_group"],
        "tut_group": subject["tut_group"],
        "repeat_subj": ""
    }

    return payload

def register(subject_to_register):
    failed_subject = {}

    for subject in subject_to_register:    
        payload = create_payload(subject_to_register[subject])

        # auto switching which sem to register
        sem = subject_to_register[subject]["sem"]
        navigate_to_sem(sem)
        register = session.post(register_url[sem-1], data=payload)

        # extracting the error message when register failed
        soup = BeautifulSoup(register.content, 'html.parser')
        # Find the <div> element with class 'alert alert-info'
        div_element = soup.find('div', class_='alert alert-info')
        # Extract the text within the <div> element
        div_text = div_element.get_text()
        # Print the extracted text
        print(div_text)

        # check if the error is due to section full already
        if "already full" in div_text.lower():
            failed_subject[subject_to_register[subject]["subject_code"]] = subject_to_register[subject]
        elif "saving" in div_text.lower():
            print("Sucessfully registered " + subject_to_register[subject]["subject_code"])

    print("")
    if len(failed_subject) > 0:
        save_json(failed_subject)

# a method to keep on trying to register a subject until someone letgo 
def register_brute_force(frequency, minute):
    failed_subject = {}
    # run x times in 10 minutes
    interval = minute * 60 / frequency
    n = 1
    for i in range(frequency):
        with open('failed_subject.json', 'r') as file:
            failed_subject = json.load(file)
        
        if len(failed_subject) > 0:
            print(f"Trying to register full section, attempt {n} of {frequency}")
            register(failed_subject)

            if i < frequency - 1:
                time.sleep(interval)
                n += 1
        else:
            break

#login to the OR system
login(login_payload)

# test your input
# test()

# uncomment register() to run the code
subject_to_take = read_subject_to_take()
# register(subject_to_take)

# retry register, specify the frequency in how many times to retry in 10 minutes
register_brute_force(10, 10)

destroy_session()