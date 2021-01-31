from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path("", views.AcmeView.as_view(), name="getting"),
]
