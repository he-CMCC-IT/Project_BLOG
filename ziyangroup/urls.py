from django.urls import path
from . import views

app_name = 'ziyangroup'
urlpatterns = [
    # ziyangroup views
    path('index/', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('image_detail/<int:id>/<slug:slug>/', views.image_detail, name='image_detail'),
]
