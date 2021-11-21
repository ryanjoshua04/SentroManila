from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('order/<int:id>/',views.order, name='order'),
    path('makeorder/<int:id>/',views.makeorder, name='makeorder')
]