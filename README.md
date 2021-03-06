# Gradpro
* Available online at http://nickalexiadis.pythonanywhere.com/

While university degrees have traditionally been seen as a big step (or even a guarantee) towards of employment, in a rapidly and ever-changing workforce such beliefs are losing ground. Technological innovations are creating new higher demands of potential employees, that necessitate ever greater fluidity in regards to the choice of career itself, as well as in the knowledge and skills involved in effectively performing in (sometimes very different) types of work.

In order to effectively prepare graduates for the future workforce, Skills Development Scotland (SDS) has proposed a model for certain skills – referred to as ‘meta-skills’ – that can provide a strong base for different types of work regardless of a person’s background. 

This project, building on pre-existing and currently in-development software, aims to provide a more comprehensive option to users who want to test their meta-skills, through a Django-based web application.The aim  is to create an interactive web application where users can complete tests and other challenges measuring these meta-skills. The system will then provide the users with visualizations of their performance in the questionnaires, as well as the average performance of all users, tracking their progress through time, as well as breaking the meta-skills down into their respective subskills.  In cases where certain skills are low, the system will also offer suggestions for improving these skills. Gradpro, as the web-app has been named, aims to serve as a prototype for a continuing education hub that will allow users to track their skills level through scientific measures and help them take appropriate steps to improve their weaker areas.
 
## Instructions
* Install a virtual environment for Python (Example: For Anaconda type “conda create -n myenv python=3.7” in the anaconda prompt)
* Activate the virtual environment (conda activate myenv)
* Install the requirements (pip install -r requirements.txt)
* Navigate to the root folder of the project
* Type “python manage.py makemigrations gradpro” and press enter
* Type “python manage.py migrate” and enter
* Type “python manage.py runserver” and press enter
* You should now be able to access the website at http://127.0.0.1:8000/
