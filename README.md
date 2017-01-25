# James Joyce digital library

This repository contains the code used for the James Joyce digital library, developed at the Centre for Manuscript Genetics of University of Antwerp. The project aims to bring together the work of many Joycean researchers and collects data from Joyce's manuscripts, notebooks, and personal library.

The website is currently in development.

## Run the site locally

If you want to be able to use the site locally, follow these steps to install the required packages and settings. This guide assumes that Python has been installed on your computer. Check if the Python package handler `pip` is correctly installed as well:

	$ python --version
	$ pip --version

The guide also assumes you have a mysqldump file in your possession that can recreate the database.

### Install the MySQL database program

The site uses the popular database tool MySQL. Install the program for your operating system via the [official website](https://dev.mysql.com/doc/refman/5.7/en/windows-installation.html). I will assume that you can access the root user with a password. To test this, see if you can gain access to the MySQL client using the following command.

	$ mysql -u root -p

### Synchronize the complete database

Save the mysqldump file in your home folder. Now log into the MySQL client using the command above. The following lines will create and reconstruct the complete database.

	mysql> create database jjdlp;
	mysql> use jjdlp;
	mysql> source mysqldump.sql;

Now that the database is ready, we can install the required code.

### Make a virtual environment (not required)

Python provides a useful tool to keep development environment separate from each other. This is called a "virtual" environment. Install this both with the package `virtualenvwrapper`, which makes it easier to work with the environments. Note that this step is not required, but is certainly 

	$ pip install virtualenv
	$ pip install virtualenvwrapper

Then in your home directory, open the file `.bashrc` (also called `.bash_profile`) and type the following lines in them:

	# where to store our virtual envs
	export WORKON_HOME=$HOME/virtualenvs
	# where projects will reside
	export PROJECT_HOME=$HOME/projects-venvs
	# where is the virtualenvwrapper.sh
	source /usr/local/bin/virtualenvwrapper.sh

Save the file. Now you should be able to create a virtualenvironment using

	$ mkvirtualenv jjdlp

This creates a new environment called "jjdlp". It must first be activated using 

	$ workon jjdlp

The `workon` command activates the virtual environment, and everything that is installed will be sealed off in it. To return outside the virtual environment write

	$ deactivate jjdlp

### Get the files and install the required packages

Copy the complete site folder (JJDLP/) to a location of your choice. (If you're in a virtualenv, this will be inside the environment's bin/ folder.) Then get into the `JJDLP/` folder and type in a terminal

	$ pip install -r requirements.txt

This will install all the necessary requirements for the site to run. The requirements file can also be found on the site's [Github repository](https://github.com/tdekeyser/jjdlp/edit/master/requirements.txt).

### Point to the correct image database folder

Now that all the requirements are installed, the site must now know where the image files are stored. Open the file `JJDLP/settings.py`, and change the value of `MEDIA_ROOT` to the path to the image database folder (starting from the root, e.g. your home directory).

	MEDIA_ROOT = os.path.join('[your/path/to/the/folder]/database', 'media')

### Point to the database

The program also needs to be able to access the database. In the `JJDLP/settings.py` file, find the variable `DATABASES` and change the value of `PASSWORD` to your own MySQL password for root user.

### Run the website

The site is now ready to be run. Open a terminal, get into the virtual environment, go to the `JJDLP/` folder and type

	$ python manage.py runserver

If all is well, the last lines of the output should be

	Django version 1.8, using settings 'JJDLP.settings'
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.

In a browser, the website will be running at `http://127.0.0.1:8000/`.

