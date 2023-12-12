from django.urls import path
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('delete-group/<str:code>/', views.deleteGroup, name='deleteGroup'),
    path('draw-name/<str:code>/', views.drawName, name='drawName'),
    path('get-person/<str:groupCode>/<str:individualCode>/', views.getPerson, name='getPerson'),
    path('create-account/', views.createAccount, name='createAccount'),
    path('new-group/', views.newGroup, name='newGroup'),
    path('reveal/', views.reveal, name='reaveal'),
    path('view-group/<str:code>', views.viewGroup, name='viewGroup'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logout'),
    path('add-participants/<str:groupName>/<str:numParticipants>/<str:budget>/', views.addParticipants, name='addParticipants'),
]