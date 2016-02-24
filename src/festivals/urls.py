from django.conf.urls import include, url


urlpatterns = [
    url(r'^phpmyadmin/', include('festivals.phpmyadmin.urls')),
]
