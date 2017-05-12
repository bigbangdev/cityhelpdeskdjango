from django.conf.urls import url
from django.contrib.auth.views import logout_then_login

urlpatterns = [

    url(r'^logout/$', logout_then_login, name="simplistic_auth_logout_then_login"),


]
