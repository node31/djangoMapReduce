from django.shortcuts import render
#from djagno.http import HttpResponse
from django.http import HttpResponse

from raw_reduce.models import *

from django_mongokit import connection,get_database

import itertools

def index(request):
	#return HttpResponse("Hello")
	return render(request,"raw_reduce/myHome.html",{})
	
def insert(request):
	
	connection.register([MyRaw])
	collName = get_database().raw
	y = collName.MyRaw()
	
	print request.POST["f_name"],'\t',request.POST["f_tags"],'\t',request.POST["f_content"]
	y.name = request.POST["f_name"]
	tag_l = request.POST["f_tags"].split(",")
	y.tags = tag_l
	y.content = request.POST["f_content"]
	y.save()
	return render(request,"raw_reduce/thankYou.html",{})
	
def perform_map_reduce(request):
	connection.register([MyRaw])
	collName = get_database().raw
	instances = collName.MyRaw.find()
	
	y = list(instances)
	
	connection.register([MyReduce])
	collName2 = get_database().reduce
	z = collName2.MyReduce()
	
	for x in y:
		z.name = map_reduce(x.name,mapper,reducer)
		#z.tags = map_reduce(x.tags,mapper,reducer)
		z.tags = x.tags #This is because logically speaking,there should be no repetition in tags
		z.content = map_reduce(x.content,mapper,reducer)
	
	return HttpResponse("Performed Map Reduce")
	
def mapper(input_value):
	l = []
	for i in input_value.split():
		l.append([i,1])
	return l
	
def reducer(intermediate_key,intermediate_value_list):
	return (intermediate_key,sum(intermediate_value_list))
	
def map_reduce(x,mapper,reducer):
	#NOTE:Here x will either be either "name","tags" or "content"
	intermediate = mapper(x)
	sorted_intermediate = sorted(intermediate)			
	groups = {}	
	for key, group in itertools.groupby(sorted_intermediate,lambda x:x[0]):
		groups[key] = list([y for x, y in group])
		
	reduced_list = [reducer(intermediate_key,groups[intermediate_key]) for intermediate_key in groups ]
	print reduced_list,'\n'
	return reduced_list

# Create your views here.
