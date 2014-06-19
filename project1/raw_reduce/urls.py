from django.conf.urls import patterns,url

from raw_reduce import views

urlpatterns = patterns('',
		url(r'^$',views.index,name = 'index'),
		url(r'^insert/$',views.insert,name = 'insert'),
		url(r'^performReduce/$',views.perform_map_reduce,name = 'perform_map_reduce'),
		url(r'^edit/$',views.edit_page,name = 'edit'),
		url(r'^edit_object/$',views.edit_object,name = 'edit_object'),
	)
