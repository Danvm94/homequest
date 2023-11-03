"""
URL configuration for homequest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from user_management.views import CustomLoginView, CustomSignupView
import homepage.views as homepage
import properties.views as properties
import profiles.views as profiles
import checkout.views as checkout

urlpatterns = [
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),

    path('accounts/signup/', CustomSignupView.as_view(),
         name='account_signup'),

    path('accounts/', include('allauth.urls')),

    path('admin/', admin.site.urls),

    path('', homepage.index_view, name='home'),

    path('about/', homepage.about_view, name='about'),

    path('properties/sale/', properties.properties_view,
         {'property_type': 'sale'}, name='properties-sale'),

    path('properties/rent/', properties.properties_view,
         {'property_type': 'rent'}, name='properties-rent'),

    path('agents/', properties.agents_view, name='agents'),

    path('profile/', profiles.profile_view, name='profile'),

    path('property/<int:property_id>/', properties.property_view,
         name='property_detail'),

    path('checkout/<int:property_id>/', checkout.checkout_view,
         name='checkout'),

    path('checkout/cache_checkout_data/', checkout.cache_checkout_data,
         name='cache_checkout_data'),

    path('checkout/success/<primary_key>', checkout.checkout_success_view,
         name='checkout_success_view'),

]
