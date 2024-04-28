from django.urls import path
from .views import LoginView, SignupView, TestTokenView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('test-token', TestTokenView.as_view(), name='test_token'),
]
