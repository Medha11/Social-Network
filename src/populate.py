import os
import socnet
os.environ["DJANGO_SETTINGS_MODULE"]= "socnet.settings"
import django
django.setup()
from basic.models import *
from django.contrib.auth.models import User
from rss.models import *
from socnet.settings import *


#creating branches and batches

it = Branch(name="Information Technology",programme="B.Tech")
cs = Branch(name = "Computer Science",programme="B.Tech")
ece = Branch(name = "Electronic And Communications",programme="B.Tech")

branches = [it,cs,ece]
branches.append(Branch(name = "Chemical",programme="B.Tech"))
branches.append(Branch(name = "Biotechnology",programme="B.Tech"))
branches.append(Branch(name = "Mechanical",programme="B.Tech"))
branches.append(Branch(name = "Production",programme="B.Tech"))
branches.append(Branch(name = "Civil",programme="B.Tech"))
branches.append(Branch(name = "Electrical",programme="B.Tech"))

years = ['1<sup>st</sup>','2<sup>nd</sup>','3<sup>rd</sup>','Final']

for branch in branches:
	branch.save()
	for year in years:
		Batch(branch=branch,year=year).save()


it3 = Batch.objects.get(branch=it,year='3<sup>rd</sup>')
cs3 = Batch.objects.get(branch=cs,year='3<sup>rd</sup>')



mca=Branch(name = "Computer Science",programme="MCA")
mba=Branch(name = "MBA",programme="MBA")
mtech=Branch(name = "Computer Science",programme="M.Tech")
branches =[mba,mca,mtech]

for branch in branches:
	branch.save()
	Batch(branch=branch,year=years[0]).save()
	Batch(branch=branch,year=years[3]).save()

Batch(branch=mba,year=years[1]).save()



#creating users
admin=User.objects.create_superuser(email="dasas@ads.com",first_name="Admin", 
					username="admin", password="root")
admin = UserProfile(user=admin,reg=str(12311232),batch=cs3,tpo=True,cpi=7)
admin.save()

sid=User.objects.create_user(email="das@ads.com",first_name="sid", last_name="patny", 
					username="sid", password="123")

sid = UserProfile(user=sid,reg=str(12312),batch=cs3,cpi=9)
sid.save()

rohit=User.objects.create_user(email="das@ads.com",first_name="rohit", last_name="thomas", 
					username="rohit", password="123")


rohit=UserProfile(user=rohit,reg=str(12122),batch=it3,cpi=8)
rohit.save()

mishra=User.objects.create_user(email="daasds@ads.com",first_name="AK", last_name="Mishra", 
					username="faculty", password="123")

mishra = UserProfile(user=mishra, role="Faculty",tpo=True)
mishra.save()



#creating courses
dbms = Course(name="DBMS",course_id="CS101")
dbms.save()

wire = Course(name="Wireless",course_id="CS1201")
wire.save()

#assigning course

Membership(member=admin,course=dbms).save()
Membership(member=mishra,course=dbms).save()
Membership(member=rohit,course=dbms).save()
Membership(member=sid,course=dbms).save()
Membership(member=admin,course=wire).save()
Membership(member=sid,course=wire).save()

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


import script

script.populate_company()