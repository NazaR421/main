from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.room_list, name='room_list'),
    path('testing/create/', views.create_booking,name = 'create_booking'),
    path("show/", views.show_calendar, name = "show_calendar"),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('testing/<int:booking_id>/cancel', views.cancel_booking, name='cancel_booking'),
    path('login/', auth_views.LoginView.as_view(template_name = 'testing/login.html'),name='login'),
    path('logout/',auth_views.LoginView.as_view(),name='logout'),
]