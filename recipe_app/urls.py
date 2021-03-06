from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send/', views.send, name='send'),
    path('signin/', views.signup_login, name='signup_login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('view/', views.show_recipe, name='show_recipe'),
    path('like/', views.like, name='like'),
    path('search/', views.search, name='search'),
    path('delete/', views.delete, name='delete'),
    path('profile/', views.profile, name='profile'),
    path('updatelog/', views.updatelog, name='updatelog')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)