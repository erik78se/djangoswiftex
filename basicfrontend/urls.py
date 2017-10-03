from django.conf.urls import url

from .views import list_view, index_view

urlpatterns = [
    url(r'^list$', list_view, name='list'),
    url(r'^$', index_view, name='index'),
]
