from django.urls import path
from Client.views import Transactions

app_name = "Client"

urlpatterns = [
    path('transaction/', Transactions.as_view(), name="transaction"),
]
