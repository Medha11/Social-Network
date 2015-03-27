from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince



#####
#####  This is to add custom filters regarding time remaining and since
#####

register = template.Library()

@register.filter
def until(value):
	now = datetime.now()

	try:
		difference = value - now
	except:
		return value

	if difference.days>0:
		return str(difference.days)+' days'
	else:
		seconds = int(difference.total_seconds())
		hours = int(seconds/3600)
		minutes = int(seconds/60)
		if hours>0:
			return str(hours)+' hours'
		elif minutes>0:
			return str(minutes)+ ' minutes'
		else:
			return str(seconds)+' seconds'





@register.filter
def age(value):
    now = datetime.now()
    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}


@register.filter
def decimate(value):
	integer = int(value)
	if integer == value:
		return str(integer)
	return str(value)