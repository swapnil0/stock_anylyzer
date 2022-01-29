from django.urls import path

from . import views

urlpatterns = [
    path('<str:symbol>', views.get_data, name='getdata'),
    path('loaddata/<str:symbol>',views.load_data,name='loaddata'),
]