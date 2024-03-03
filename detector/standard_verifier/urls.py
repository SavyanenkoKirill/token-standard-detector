from . import views
from django.urls import path

urlpatterns = [
    path("", views.verify_contract, name='verify_contract')
]
