import os
import socnet
os.environ["DJANGO_SETTINGS_MODULE"]= "socnet.settings"
import django
django.setup()
from basic.models import *
from django.contrib.auth.models import User
from rss.models import *

#creating users
admin=User.objects.create_superuser(email="dasas@ads.com",first_name="Admin", 
					username="admin", password="root")
admin = UserProfile(user=admin,reg=str(12311232))
admin.save()

sid=User.objects.create_user(email="das@ads.com",first_name="sid", last_name="patny", 
					username="sid", password="123")

sid = UserProfile(user=sid,reg=str(12312))
sid.save()

rohit=User.objects.create_user(email="das@ads.com",first_name="rohit", last_name="thomas", 
					username="rohit", password="123")


rohit=UserProfile(user=rohit,reg=str(12122))
rohit.save()

mishra=User.objects.create_user(email="daasds@ads.com",first_name="AK", last_name="Mishra", 
					username="faculty", password="123")

mishra = UserProfile(user=mishra, role="Faculty")
mishra.save()



#creating courses
dbms = Course(name="DBMS",course_id="CS101")
dbms.save()

wire = Course(name="Wireless",course_id="CS1201")
wire.save()

#assigning course

Membership(student=admin,course=dbms).save()
Membership(student=mishra,course=dbms).save()
Membership(student=rohit,course=dbms).save()
Membership(student=sid,course=dbms).save()
Membership(student=admin,course=wire).save()
Membership(student=sid,course=wire).save()

#creating topics
tech = Topic(name="Tech")
tech.save()
fin = Topic(name="Finance")
fin.save()

#adding interests
Interest(topic=tech, student=admin).save()
Interest(topic=tech, student=rohit).save()
Interest(topic=tech, student=sid).save()
Interest(topic=tech, student=mishra).save()
Interest(topic=fin, student=admin).save()
Interest(topic=fin, student=sid).save()


