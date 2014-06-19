from django.shortcuts import render
#from djagno.http import HttpResponse
from django.http import HttpResponse

from raw_reduce.models import *

from django_mongokit import connection,get_database

import itertools

from bson.objectid import ObjectId

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
	
	name_id = "name"
	tag_id = "tags"
	content_id = "content"
	
	obj = collName.MyRaw.find({name_id:request.POST["f_name"],content_id:request.POST["f_content"]})
	obj_l = list(obj)
	
	for i in obj_l:
		obj_id = str(i._id)
		
	print obj_id
	#After Saving this it is important that we also include it in "to_reduce" collction
	
	collName2 = get_database().to_reduce
	z = collName2.ToReduce()
	z._id = ObjectId(obj_id)
	z.save()
	return render(request,"raw_reduce/thankYou.html",{})
	
"""
def perform_map_reduce(request):
	
	connection.register([MyRaw])
	collName = get_database().raw
	instances = collName.MyRaw.find()
	
	y = list(instances)
	
	connection.register([MyReduce])
	collName2 = get_database().reduce
	z = collName2.MyReduce()
	
	for x in y:
		z.name = dict(map_reduce(x.name,mapper,reducer))
		print "name..................................", z.name
		#z.tags = map_reduce(x.tags,mapper,reducer)
		z.tags = x.tags #This is because logically speaking,there should be no repetition in tags
		z.content = dict(map_reduce(x.content,mapper,reducer)) 
		z.orignal = x._id
		z.save()
		#You have to make sure that no key contains "." because this proves an error
	
	return HttpResponse("Performed Map Reduce")


"""

def perform_map_reduce(request):
	#db = get_database()
	#gs_collection = db[GSystem.collection_name]

	#connection.register([ToReduce])	
	collName = get_database()["to_reduce"]
	instances = collName.ToReduce.find()
	y = list(instances)
	
	#connection.register([MyReduce])
	collName2 = get_database()["reduce"]
	
	
	#connection.register([MyRaw])
	collName3 = get_database()["raw"]
	
	
	for x in y:
		z = collName2.MyReduce()
		orignal_doc = collName3.MyRaw.find_one({"_id":x._id})
		z_old = collName2.MyReduce.find_one({"orignal":x._id})
		
		print "ORIGNAL DOC >>>>>>>>>>>>>>>>>>>>>>>>",orignal_doc		
		
		if z_old:
			print "OLD DOC >>>>>>>>>>>>>>>>>>>>> ",z_old
			#z_old.name = dict(map_reduce(orignal_doc.name,mapper,reducer))
			#z_old.tags = orignal_doc.tags
			#z_old.content = dict(map_reduce(orignal_doc.content,mapper,reducer))
			#z_old.save()
			#collName2.MyReduce.remove({"orignal":x._id})
			z_old.delete()
			
		
		z.name = dict(map_reduce(orignal_doc.name,mapper,reducer))
		#z.name = list(dict(map_reduce(orignal_doc.name,mapper,reducer)))
		z.tags = orignal_doc.tags
		z.content = dict(map_reduce(orignal_doc.content,mapper,reducer))
		#z.content = list(dict(map_reduce(orignal_doc.content,mapper,reducer)))
		z.orignal = x._id
		print "NAME>>>>>>>>>>>>>>>>>",z.name
		print "CONTENT>>>>>>>>>>>>>>",z.content
		z.save()
		print "OKOKOKOKK"
		x.delete()
	
	
	return render(request,"raw_reduce/thankYou.html",{"name":"pranav"})

		
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
	
def edit_page(request):
	#return HttpResponse("Edit")
	return render(request,"raw_reduce/edit_page.html",{})

def edit_object(request):
	#return HttpResponse("Edit Object")
	#This function mimics the difficulties we are going to have in implementing edit_object functionality
	#The user comes and edits a particular object
	#The object will be edited but what about the map reduce.
	#We will again have to perform map reduce on it
	#But performing map reduce with each edit will be very tedious
	#Thus, we will have to perform map reduce as a cron job
	#Thus, we will have to maintain a log of object id's on which we want to perform map reduce
	#Thus, this function will edit the object and then lodge that objectID in a new collection named as "to_reduce"
	
	#It is possible that there are more than one update before you run your cron job
	#Thus, make sure that you check that the object Id is not already present in the "to_reduce" collection before inserting it
	
	connection.register([MyRaw])
	collName = get_database().raw
	obj = ObjectId(request.POST["f_id"])
	print obj
	instances = collName.MyRaw.find({"_id":obj})
	y = list(instances)
	print y
	
	for z in y:
		z.name = request.POST["f_name"]	
		z.tags = request.POST["f_tags"].split(",")
		z.content = request.POST["f_content"]
		z.save()
		
	collName2 = get_database().to_reduce
	
	instances = collName2.ToReduce.find({"_id":obj})
	y = list(instances)
	
	if not y:
		x = collName2.ToReduce()
		x._id = obj
		x.save()	
	
	return render(request,"raw_reduce/thankYou.html",{})

# Create your views here.
