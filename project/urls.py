"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings 
from django.conf.urls.static import static
from core.views import CashOperationsListView, ReportsView, add_client, client_detail, client_list, edit_client, export_reports, freeze_membership, login_view, logout_view, membership_type_info, protected_view, refund_membership, sell_card, sell_one_time_membership, unfreeze_membership, withdraw_cash
urlpatterns = [
    path('', client_list, name='client_list'),
    path('admin/', admin.site.urls),
    path('clients/add/', add_client, name='add_client'),
    path('clients/<int:pk>/', client_detail, name='client_detail'),
    path('api/membershiptypes/<int:pk>/', membership_type_info, name='membership_type_info'),
    path('membership/<int:pk>/freeze/', freeze_membership, name='freeze_membership'),
    path('membership/<int:pk>/unfreeze/', unfreeze_membership, name='unfreeze_membership'),
    path('membership/<int:pk>/refund/', refund_membership, name='refund_membership'),
    path('reports/export/', export_reports, name='export_reports'),
    path('reports/', ReportsView.as_view(), name='reports'),
    path('cash-operations/', CashOperationsListView.as_view(), name='cash_operations'),
    path('sell-card/', sell_card, name='sell_card'),
    path('withdraw-cash/', withdraw_cash, name='withdraw_cash'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('sell-one-time/', sell_one_time_membership, name='sell_one_time_membership'),
    # Пример защищенного маршрута
    path('client/edit/<int:client_id>/', edit_client, name='edit_client'),
    path('protected/', protected_view, name='protected'),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
