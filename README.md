
  

# Disclaimer

I will not guarantee the successful of registering a subject.

I will not responsible if you failed to register a subject

  

## Setting up

Run `pip install -r requirements.txt`

  

## Preparing Your Information

### Preparing your login information

Create a text file named `credential.txt`

copy the following text

```

MATRICID=YOURMATRICID

PASSWORD=PASSWORD

```

replace `YOURMATRICID` with your matric ID

replace `PASSWORD` with your password

  

### Preparing the subject to register

In the file `subject_to_take.csv` file, list down the subjects you want to register.

Format the information in the following way:

If you want to register for BCS3133 section 01B in semester 1:

`1,BCS3133,01,01B`

If a university course does not have a lab section, you need to mention P in the section:

`1,UHF2121,01P,01P`

refer `subject_to_take_example.csv` for more example

  

## Testing before executing the code

### Testing Your Information

Run the `test()` function to check your information.

Check the terminal output, make sure it is correct.

If not go back and change the CSV file again.

  

### Testing Your Login And Navigation

A `login_test.html`, `sem_1_page.html` and `sem_2_page.html` file will be created at your folder when you run test()

Open them in your browser and check if you successfully login to the OR

  

## Running the Code

### Registering subject

Uncomment the `register()` function to execute the code and register for the subjects.

Subject that already full will failed to register and will be saved as JSON file in your directory, refer below for further steps

Refresh OR to double check your subject

  

### Brute forcing subject register

If you failed to register a subject because a section is already full, you can try to brute force to retry it

Make sure that your failed subject total credit hour is less than 20 with the subject that you registered earlier

run `register_brute_force()`

specify `frequency` and `minute`in minutes

this will tell the program to retry how many times in how much time

example:

when `frequency = 10` and `minute = 10`

the program will retry 10 times in 10 minutes

OR

the program will retry 1 time in every 1 minute for 10 times

**Do not use too high frequency, may cause troubles**
