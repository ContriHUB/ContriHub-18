# ContriHub-18
  
  ContriHUB is an event where we are expecting to get more and more people involved in Open Source activities.

### Instructions to run Project locally

## Linux

  #### Installing Python.
    - `$ sudo apt-get install python-pip python-dev build-essential`
    - `$ apt install Python3.6`
    - `use easy_install for older versions of ubuntu e.g -$ easy_install python3-pip`
    - `$ apt install python3-pip`
    
  #### Creating virtual environment activating and deactivating it
	## Creating Virtual environment
	# Python 2:
    - `$ virtualenv env`
  # Python 3:
    - `$ python3 -m venv env`
  ## Activating virtual environment
  	- `$ source env/bin/activate`
  ## Deactivating virtual environment
  	- `(env) $ deactivate`
    
  #### Installing all the requirements and mention if their are some exceptions while installations
    - `$ pip install requirements.txt`

  #### Any changes if required in ContriHub/settings.py for running project in local like tell how to setup some environment        variables used in ContriHub/settings.py file.

  #### How to setup(Install/create_db/configure) different databases like Postgresql, Mysql, sqlite.
    - `As per current settings you don't need to make any change in settings.py if you don't have an environment variable set       as 'DATABASE_URL' ` 
    - `$ python manage.py makemigrations`
    - `$ python manage.py migrate`
    
  #### Running Project
    - `$ Python manage.py runserver`
    - `$ visit 127.0.0.1:8000`

  #### How to deploy?
    - `$ Here goes instructions`
    

## Windows

  #### Installing Python.
    - `download python-X.exe file from [Download](https://www.python.org/downloads/) page of official website`
    - `double click the downloaded file`
    - `the setup installation wizard will guide you through installation process`
    - `Ensure that python.exe is added to PATH. Adding Python to the PATH will allow you to call if from the command line.`
    - `Installing pip`
    - `Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)  being careful to save it as a .py file rather than .txt. Then, run it from the command prompt:`
    - `$ python get-pip.py`
    
  #### Creating virtual environment activating and deactivating it
    - `Install virtualenv package `
    - `$ pip install virtualenv`
    - `Creating virtual environment`
    - `$ mkvirtualenv *env_name*`
    - `Activating virtual environment`
    - `$ setprojectdir .`
    - `Deactivating virtual environment`
    - `$ deactivate`
    

  #### Installing all the requirements and mention if their are some exceptions while installations
	- `run the command from cmd`
    - `$ pip install -r requirements.txt`

  #### Any changes if required in ContriHub/settings.py for running project in local like tell how to setup some environment        variables used in ContriHub/settings.py file.
    
  #### How to setup(Install/create_db/configure) different databases like Postgresql, Mysql, sqlite.
    - `$ Here goes instructions`
    
  #### Running Project
    - `$ Python manage.py runserver`

  #### How to deploy?
    - `$ Here goes instructions`
    
    
## Mac

  #### Installing Python.
    - `Install XCode from Apple store`
    - `open Terminal and install *Homebrew* and then install python`
    - `$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    - `$ brew install python`
    
  #### Creating virtual environment activating and deactivating it
    - `Installing virtual environment`
    - `pip install virtualenv`
    - `Create a virtual environment for a project:`
	- `$ cd my_project_folder`
	- `$ virtualenv my_project`
	- `Activating virtual environment`
	- `$ source my_project/bin/activate`
	- `deactivating virtual environment`
	- `$ deactivate`

  #### Installing all the requirements and mention if their are some exceptions while installations
    - `$ pip install -r requirements.txt`

  #### Any changes if required in ContriHub/settings.py for running project in local like tell how to setup some environment        variables used in ContriHub/settings.py file.
    - `$ Here goes instructions`
    
  #### How to setup(Install/create_db/configure) different databases like Postgresql, Mysql, sqlite.
    - `$ Here goes instructions`
    
  #### Running Project
    - `$ Here goes instructions`

  #### How to deploy?
    - `$ Here goes instructions`


Deploy on Heroku - 

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

<h3>Contact ContriHUB Admins </h3>

<a href="mailto:deepakbharti@mnnit.ac.in">Deepak Bharti</a><br>
<a href="mailto:abhey.mmnit@gmail.com">Abhey Rana</a><br>
<a href="mailto:akshay31057@gmail.com">Akshay Sharma</a>
