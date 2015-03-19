TODO
-> Upvotes and downvotes for answers
-> Sorting answers according to votes, date
-> Badges for questions not viewed



-> Proper profiles
-> Course assigning interface for adding professors and students to course(optional)
-> Answers statistics

-> TPO views

DONE

-> Assignment submission 
-> Optional multiple files
-> File name display for uploads
-> Deadline countdown
-> Proper date time conversions
-> Follow button for questions and proper notifications on new answers
-> Dynamic notifications
-> Upload assignment solutions
-> Assignment Overview for professor


Instructions

Download the whole thing using git clone i think

there is an activate file in bin/

$ source bin/activate 

This starts the virtualenv

the manage.py is in src/

Before runserver do a migrate, make sure to create a database socnet i think
then run a createsuperuser to create an admin

run admin site using 127.0.0.1:8000/admin
Try the register process in the homepage by entering your mnnit.ac.in email 
Also make sure the internet is working in order to send a mail

Main website at 127.0.0.1:8000

It is advised not to use the admin to login 

The UserProfile model has a User model object and reg. no etc. This will have all the fields that we want to include in a user

Create course using admin site to start using forums
Also add membership objects in the admin site to link user to course

The templates folder contains the htmls sorted acc. to app
The static folder contains the css, js and images

Still working on notifications and file handling, assignments etc.

Feel free to change the html although i think we'll need a design revamp. Was just learning the stuff so forgive me if the design sucks

any doubts FB. So it begins finally!!

There maybe glitches as I had to create a new project and transfer. So let me know.
