# ICSPScheduler
Scheduler for the International Cultural Service Program at the University of Oregon

All application code can be found in code directory <br>
All coverage testing code can be found tests directory <br>
Program can be run from command line by typing <br>
python main.py <br>
Our program requires Python3, PIP or equivalent package installer, Tkinter package, and IntervalTree<br>
<br>
Please see the User Guide for additional information<br>




RUN TESTS:

To run tests, type in the following on the command line from root directory

python -m unittest discover

To run with coverage, type in:
Uncomment the imports in __init__.py from /code


coverage run -m unittest discover
coverage html

(Click in the html file created to view the coverage of the program)

Remember to comment out the imports in /code/__init__.py after testing for main to work
