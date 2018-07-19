from django.conf.urls import url

from payments import views

app_name = 'payments'

urlpatterns = [
    url(r'^$', views.plans),
    url(r'^subscribe', views.subscribe),
]