"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from crypto.views import CryptoDataList  # Ubah impor ini
from crypto.views import CryptoDataDetail
from forex.views import ForexDataList  # Ubah impor ini
from forex.views import ForexDataDetail
from stocks.views import StockDataList  # Ubah impor ini
from stocks.views import StockDataDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/crypto_data/', CryptoDataList.as_view()),  # Gunakan CryptoDataList di sini
    path('api/crypto_data/<str:symbol>/', CryptoDataDetail.as_view()),
    path('api/forex_data/', ForexDataList.as_view()),  # Gunakan ForexDataList di sini
    path('api/forex_data/<str:symbol>/', ForexDataDetail.as_view()),
    path('api/stock_data/', StockDataList.as_view()),  # Gunakan ForexDataList di sini
    path('api/stock_data/<str:symbol>/', StockDataDetail.as_view()),
]

