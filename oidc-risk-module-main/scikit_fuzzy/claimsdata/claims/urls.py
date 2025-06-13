# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('education/', views.education_claim_list, name='education_claim_list'),
    path('osp/', views.osp_claim_list, name='osp_claim_list'),
    path('education/add/', views.add_education_claim, name='add_education_claim'),
    path('osp/add/', views.add_osp_claim, name='add_osp_claim'),

    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),

    # New URL patterns for Flask interactions
    path('api/transactions/add/', views.add_transaction_api, name='add_transaction_api'),
    path('api/transactions/<str:name>/', views.get_transaction_api, name='get_transaction_api'),
    path('api/transactions/update/<int:pk>/', views.update_transaction_api, name='update_transaction'),

    # Existing API endpoint for claims data
    path('api/claims/<str:table_name>/', views.get_claims_data, name='get_claims_data'),
]
