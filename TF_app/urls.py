from django.urls import path
from . import views
urlpatterns = [
    path('',views.index_view,name='index'),
    path('login',views.login_view,name='login'),
    path('register',views.register_view,name='register'),
    path('send_done',views.link_send_view,name='link_send'),
    path('activate/<slug:uid>/<slug:token>/',views.link_active_view,name='activate'),
]