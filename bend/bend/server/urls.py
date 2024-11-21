"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app.endpoints.accounts.create_account_view import CreateAccountView
from app.endpoints.returns.return_view import ReturnView
from app.endpoints.returns.submit_return_view import SubmitReturnView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account', CreateAccountView.as_view(), name='create-account'),
    path('return', ReturnView.as_view(), name='create-return'),
    path('return/<uuid:return_id>', ReturnView.as_view(), name='update-return'),
    path('submit', SubmitReturnView.as_view(), name='submit-return'),
]
