from django.urls import path
from .views import RegisterView, LoginView, UploadFileView, PredictView
from .views import UploadFileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # -----------Protected----------
    path('upload/', UploadFileView.as_view(), name='upload-file'),
    path('predict/', PredictView.as_view(), name='predict'),
]
