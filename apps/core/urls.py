from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (IndexView,
                    IntranetView,
                    LoginView,
                    RegistrationFormView,
                    SuccessView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registrar/', RegistrationFormView.as_view(), name='registrar'),
    path('success/', SuccessView.as_view(), name='success'),
    path('intranet/', IntranetView.as_view(), name='intranet'),
]
