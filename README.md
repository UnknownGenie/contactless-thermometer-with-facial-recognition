# contactless-thermometer-with-facial-recognition

This project uses Azure Face API to perform facial recognition.

RaspberryPi is used to process and generate API calls.

Temperature sensor is used to determine temeprature.

A web interface is provided to interact with RaspberryPi./n

# Usage
1. git clone https://github.com/UnknownGenie/contactless-thermometer-with-facial-recognition
2. cd contactless-thermometer-with-facial-recognition
3. Now look at train_data. Place your training data, the images for each person in respective folder. Note directory name will be considered as 
person name. Person Group is a container of multpile people, MAX of 1000 people can be used in single person group. Again Person Group directory name will be considered as person group name.
Look for further details at: https://github.com/UnknownGenie/contactless-thermometer-with-facial-recognition/blob/master/train_data/README.md
4. Follow the same process for testing data (if any). Person Group directory's folder name must correspond to those in train_data. Place images of persons to be identfied under the respective person group directory. 
Look for further details: https://github.com/UnknownGenie/contactless-thermometer-with-facial-recognition/blob/master/test_data/README.md
3. pip install -r requirements.txt
4. python main.py

# Workflow
Program will initialize a database at first run. Train and Test all given images under train_data and test_data directories. It executes two watchdogs (callbacks to look for new file creation) on both test and train directories. In case of any new file, respetive function will be executed. User can look at logs generated on terminal.

# Note
Tested on Anaconda with Windows 10, report for any errors on other platforms.

