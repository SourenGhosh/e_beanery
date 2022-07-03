from django.urls import path, re_path, include
from base.views import index, ViewOrder, ViewTable, BillingDetails

urlpatterns = [
    path("index/", index, name = "test"),
    path('api/order', ViewOrder.as_view()),
    path('api/empty_table', ViewTable.as_view()),
    path('api/billing', BillingDetails.as_view())
]