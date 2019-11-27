

app name: 10MWT
language: Python
Test: Based off 10 meter walk test

Details:

> Can record up to three trials per patient starting and stopping and reseting until saved
> When third trial is done json object is created and writes to a txt file to store data locally on your machine
> "Search for patient" functionality works basically by searching these files and then displaying the test data if found
> Search for patient will not work until at least one test has been run, for obvious reasons
> New test cannot be saved without patient name 
> New test basically just restarts the app for a fresh start
> Gait speed is displayed per trial and average is shown at the end

Instructions:

1. file is .py so can be run via cmd
2. create new patiant i.e. "Frodo"
3. save three trials
4. frodo.txt is created
5. search for patient: "Frodo"
6. see json object displayed
