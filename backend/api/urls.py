from django.urls import path
from .views import RegisterView, LoginView, MainPageView
from .views import UploadFileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('main/', MainPageView.as_view(), name='main'),
    path('upload/', UploadFileView.as_view(), name='upload-file'),
]
