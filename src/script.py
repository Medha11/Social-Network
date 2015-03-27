# -*- coding: utf-8 -*-

import os
import socnet
os.environ["DJANGO_SETTINGS_MODULE"]= "socnet.settings"
import django
django.setup()
from tpo.models import *
from socnet.settings import *
from django.core.files import File


def populate_company():
	BASE = os.path.join(BASE_DIR,'static','company')
	file_path = os.path.join(BASE,'amazon.jpg')
	logo=open(file_path, 'r')

	name = 'Amazon'
	summary = 'Amazon.com, Inc. is an American electronic commerce company with headquarters in Seattle, Washington. It is the largest Internet-based retailer in the United States. Amazon.com started as an online bookstore, but soon diversified, selling DVDs, VHSs, CDs, video and MP3 downloads/streaming, software, video games, electronics, apparel, furniture, food, toys, and jewelry. The company also produces consumer electronics—notably, Amazon Kindle e-book readers, Fire tablets, Fire TV and Fire Phone — and is a major provider of cloud computing services. Amazon also sells certain low-end products like USB cables under its inhouse brand AmazonBasics.'
	website = 'www.amazon.com'
	company = Company(name=name,summary=summary,website=website)

	company.logo.save('amazon.jpg',File(logo))
	company.save()

	name = 'Google'
	summary = 'Google is an American multinational corporation specializing in Internet-related services and products. These include online advertising technologies, search, cloud computing, and software. Most of its profits are derived from AdWords, an online advertising service that places advertising near the list of search results. Google was founded by Larry Page and Sergey Brin while they were Ph.D. students at Stanford University. Together they own about 14 percent of its shares but control 56 percent of the stockholder voting power through supervoting stock. '
	website = 'www.google.com'
	company = Company(name=name,summary=summary,website=website)

	file_path = os.path.join(BASE,'google.png')
	logo=open(file_path, 'r')
	company.logo.save('google',File(logo))
	company.save()

	name = 'Flipkart'
	website = 'www.flipkart.com'
	summary = 'Flipkart, is an E-Commerce company established in 2007 by Sachin Bansal and Binny Bansal. It is registered in Singapore, with headquarters at Bangalore, Karnataka. Flipkart has launched its own product range under the name "DigiFlip" with products including tablets, USBs, and laptop bags. In May 2014, Flipkart received $210 million from DST Global and in July it raised $1 billion led by existing investors Tiger Global and South Africa\'s media group Naspers. Flipkart\'s last fundraising round in December had pegged its valuation at $12 billion.'
	company = Company(name=name,summary=summary,website=website)

	file_path = os.path.join(BASE,'flipkart.jpeg')
	logo=open(file_path, 'r')
	company.logo.save('flipkart',File(logo))
	company.save()





