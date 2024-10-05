from django.urls import path
from .views import RegisterView, LoginView, MainPageView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('main/', MainPageView.as_view(), name='main'),
]
