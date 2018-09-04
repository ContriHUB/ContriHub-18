# ContriHub-18
OpenSource is an event under Avishkar-18 where we are expecting to get more and more people involved in Open Source activities.


### Instructions to run locally

1. Install Python and some dev tools for Python 
  - $ sudo apt-get install python-pip python-dev build-essential 
  - $ apt install Python3.6
  - use easy_install for older versions of ubuntu e.g -$ easy_install python3-pip
  
2. Install Pip
  - apt install python3-pip

3. Install other requirements given in requirements.txt file
  - pip install requirements.txt

4. Modify database engine,
  - Comment line 100-114 in settings.py 
  - uncomment line 115-120
  - save changes

5. sync db
  - python manage.py makemigrations
  - python manage.py migrate

6. runserver
  - Python manage.py runserver
  - visit 127.0.0.1:8000

7. Done :-)



Deploy on Heroku - 

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

<h3>Contact ContriHUB Admins </h3>

<a href="mailto:deepakbharti@mnnit.ac.in">Deepak Bharti</a><br>
<a href="mailto:abhey.mmnit@gmail.com">Abhey Rana</a><br>
<a href="mailto:akshay31057@gmail.com">Akshay Sharma</a>
