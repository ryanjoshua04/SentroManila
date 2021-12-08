from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('order/<int:id>/',views.order, name='order'),
    path('makeorder/<int:id>/<str:name>',views.makeorder, name='makeorder'),
    path('otp_confirmation/<int:id>/<str:name>', views.otp_confirmation, name='otp_confirmation'),
    path('search/', views.searchItem, name='searchItem')
]