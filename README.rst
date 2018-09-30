.. _github: https://github.com/shustinm/microrepo

*********
Microrepo
*********

Create a local pypi repository to use pip off-line.

.. contents:: 

Minirepo is a command-line program that downloads Python packages from pypi.python.org_, so you can use pip_ without internet. I needed to maintain a python repository in an isolated cluster environment, and after trying several tools to mirror pypi index, I dedided to make my own tool. 

Some mirroring tools such us bandersnatch_ didn't meet my requirements, because I wanted to do a selective mirror, only downlowing all sources for python 2.7, for example. Bandersnatch gets the full content, about 140GB at the time of my first version of microrepo.

Then I was inspired by basket_, which is almost what I wanted, but you need to specify the list of packages to download. I ended up using the json API to get the packages that I needed, and then calling basket to download or update the packages. In the end, that approach was slow and buggy, so I wrote this small program to do what I just needed. Now, my microrepo folder has about 12GB with only the latest packages, and it takes about 20 minutes to mirror.


Installation
============

Download and install
-----------------------


Use git:

.. code:: bash

    $ git clone https://github.com/shustinm/microrepo
    $ cd microrepo
    $ python setup.py install


Usage
=====

.. code::
	
	# run it from the command line:
	$ microrepo

	# or run the python script if you didn't install it:
	$ ./microrepo.py

The firt time it's executed, the program will ask you for the local repository path, which defaults to ~/microrepo in Linux. A json configuration file is created and saved as ~/.microrepo, that you can edit to your preferences. This configuration file looks like this:

.. code:: javascript

	{
		"processes"       : 20, 
		"repository"      : "/home/user/microrepo"
		"package_types"   : ["bdist_egg","bdist_wheel","sdist"], 
		"extensions"      : ["bz2","egg","gz","tgz","whl","zip"], 
		"python_versions" : ["2.7","any","cp27","py2","py27","source"], 
	}


Minirepo uses packages_types, extensions, and python_versions as filters. I was analysing the full list of packages available in pypi.python.org_, and it looks that all the options are something like the list below, you can try any other option. For me, I was only interested in python 2.7 packages, sources, wheels and eegs distributions, and some extensions.
/mini

.. code:: python

	PYTHON_VERSIONS = [
		'2', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.7.6', '3.0', '3.1', 
		'3.2', '3.3', '3.4', '3.5', 'any', 'cp25', 'cp26', 'cp27', 'cp31', 
		'cp32', 'cp33', 'cp34', 'cp35', 'py2', 'py2.py3', 'py26', 'py27', 
		'py3', 'py32, py33, py34', 'py33', 'py34', 'python', 'source'
	]
	
	PACKAGE_TYPES = [
		'bdist_dmg', 'bdist_dumb', 'bdist_egg', 'bdist_msi', 'bdist_rpm', 
		'bdist_wheel', 'bdist_wininst', 'sdist'
	]
	
	EXTENSIONS = [
		'bz2', 'deb', 'dmg', 'egg', 'exe', 'gz', 'msi', 'rpm', 'tgz', 'whl', 'zip'
	]


Use pip without internet
========================

.. code:: bash

	$ pip install --no-index --find-links=/home/user/microrepo <package-name>


I prefer to setup environment variables in my profile so I don't have to provide extra command line arguments.

.. code:: bash

	# save these 2 variable in your profile 
	$ export PIP_NO_INDEX=true
	$ export PIP_FIND_LINKS=/home/user/microrepo
	
	# then run pip as usual
	$ pip install <package-name>



