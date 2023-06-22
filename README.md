# Disclaimer

    I will not guarantee the sucessfull of registerring a subject.
    I will not responsible if you failed to register a subject

## Setting up

    Run pip install -r requirements.txt

## Preparing Your Information

    Create a subject_to_take.csv file listing down the subjects you want to register for.
    Format the information in the following way:
        If you want to register for BCS3133 section 01B in semester 1:
            1,BCS3133,01,01B
        If a university course does not have a lab section, you need to mention P in the section:
            1,UHF2121,01P,01P
    refer subject_to_take_example.csv for more info

## Updating Your Information in the Python File

    Open the Python file and modify the login_payload dictionary with your login credentials.
    Leave the commit field as it is.

    login_payload = {
        "txtUsername": "YOUR USERNAME",
        "txtPassword": "YOUR PASSWORD",
        "commit": ""  
    }

## Testing Your Information

    Run the test() function to check your information.
    Check the terminal output, make sure it is correct.
    If not go back and change the CSV file again.

## Testing Your Login

    A login_test.html, sem_1_page.html and sem_2_page.html file will be created at your folder when you run test()
    Open them in your browser and check if you successfully login to the OR

## Running the Code

    Uncomment the register() function to execute the code and register for the subjects.
