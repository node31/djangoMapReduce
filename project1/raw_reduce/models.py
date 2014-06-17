from django.db import models

from django_mongokit import connection
from django_mongokit.document import DjangoDocument

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
		'name':[dict],
		'tags':[dict],
		'content':[dict],
	}
	use_dot_notation = True
	
connection.register([MyReduce])	


# Create your models here.
