from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_recommended_users),
    path('friends/', views.get_my_friends),
    path('friend-request/<int:id>/', views.send_friend_request),
    path('friend-request/<int:id>/accept/', views.accept_friend_request),
    path('friend-requests/', views.get_friend_requests),
    path('outgoing-friend-requests/', views.get_outgoing_friend_requests),
]
