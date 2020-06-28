#   @@@@@@@@@@@@@@@@@@@@@@@@
#   **Code by Aron Talai****
#   @@@@@@@@@@@@@@@@@@@@@@@@

# Various datetime utilities

# def libs
import datetime
from dateutil.parser import parse
import calendar


# def func
def current_time():
	'''print current datetime'''	
	return datetime.datetime.now() # date with hours, mins, and seconds
	#return datetime.date.today() # just date

def unix_2_dt(unix_time_stamp):
	'''Convert unix time stamps to datetime'''
	mydatetime = datetime.datetime.fromtimestamp(unix_time_stamp)
	return mydatetime

def dt_2_unix(datetime_object):
	'''converts date time object into unix time stamp'''
	unix_time_stamp = int(datetime_object.timestamp())
	return unix_time_stamp

def string_2_dt(input_string):
	'''returns a datetime from a flexible input_string that indicates date
	the input string has a lot of flexibility'''
	return parse(input_string)

def reformat_dt_object_string(datetime_datetime_object, string_format):
	'''reformats datatime objects to a string based on string_format'''
	# example dt = datetime.datetime(2001, 1, 31, 10, 51, 0) 
	# string_format = '%Y-%m-%d::%H-%M'
	return datetime_datetime_object.strftime(string_format)

def make_time_delta(delta_type, duration):

	if delta_type == 0: return datetime.timedelta(weeks = duration)
	if delta_type == 1: return datetime.timedelta(days = duration)
	if delta_type == 2: return datetime.timedelta(hours = duration)
	if delta_type == 3: return datetime.timedelta(minutes = duration)
	if delta_type == 4: return datetime.timedelta(seconds = duration)

def make_flexible_time_delta(week_duration,day_duration,hour_duration,minute_duration ):
	return datetime.timedelta(weeks=week_duration, days=day_duration, hours=hour_duration, minutes=minute_duration)

# # Example 1
# # How many days has it been since your birthday
# bday = 'Sep 9, 1993'  # use bday
# print (current_time() - string_2_dt(bday))


# # Example 2: 
# # count the number of Saturdays between start date and end date 
# start_date = datetime.date(1869, 1, 2)
# end_date = datetime.date(1869, 10, 2)


# range_diff = datetime.date(1869, 10, 2) - datetime.date(1869, 1, 2)

# count = 0
# for cuurent_date in (start_date + make_time_delta(1,n) for n in range(range_diff.days + 1)):

# 	if calendar.day_name[cuurent_date.weekday()] == 'Saturday':
# 		count = count + 1
# print (count)

# ## Example 3: 
# ## How many days is it until your next birthday this year? (easy)
# bday = 'Sep 9, 1993'  # use bday
# bday_this_year = '{}, {}'.format(bday.split(',')[0], current_time().year)
# diff = string_2_dt(bday_this_year) - current_time()
# print (diff.days)

# # Example 4
# # Count the number of days between successive days in the following list. (medium)
# input_dates = ['Oct, 2, 1869', 'Oct, 10, 1869', 'Oct, 15, 1869', 'Oct, 20, 1869', 'Oct, 23, 1869']
# differences = [(string_2_dt(input_dates[i+1]) - string_2_dt(input_dates[i])).days 
# 				for i in range(0,len(input_dates)-1) ]
# print (differences)