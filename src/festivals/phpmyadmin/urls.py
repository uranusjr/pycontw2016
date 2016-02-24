from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?:index\.php)?$', views.index, name='phpmyadmin_index'),
    url(r'^url\.php$', views.url_redirect),
    url(r'^(?P<path>.+\.(?:css|gif|ico|png))(?:\.php)?$', views.staticfile),
]
