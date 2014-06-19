from django.db import models

from django_mongokit import connection
from django_mongokit.document import DjangoDocument

from bson import ObjectId

class MyRaw(DjangoDocument):
	structure = {
		'name':unicode,
		'tags':[unicode],
		'content':unicode,
	}
	use_dot_notation = True

connection.register([MyRaw])

class MyReduce(DjangoDocument):
	structure = {
		'name':dict,
		'tags':[unicode],
		'content':dict,
		'orignal':ObjectId #This is the objectId of that object whose map reduce we have performed
	}
	use_dot_notation = True
	
connection.register([MyReduce])	

class ToReduce(DjangoDocument):
	structure = {
		'_id':ObjectId
	}
	use_dot_notation = True
connection.register([ToReduce])


# Create your models here.
