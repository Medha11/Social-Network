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
		ans =  str(difference.days)+' day'
		if difference.days > 1:
				ans+='s'
		return ans
	else:
		seconds = int(difference.total_seconds())
		if seconds < 0:
			return 'Over'
		hours = int(seconds/3600)
		minutes = int(seconds/60)
		if hours>0:
			ans = str(hours)+' hour'
			if hours>1:
				ans+='s'
			return ans

		elif minutes>0:
			ans = str(minutes)+ ' minute'
			if minutes>1:
				ans+='s'
			return ans
		else:
			ans = str(seconds)+' second'
			if seconds>1:
				ans+='s'
			return ans





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
	value = float(value)
	integer = int(value)
	if integer == value:
		return str(integer)

	return str(value)