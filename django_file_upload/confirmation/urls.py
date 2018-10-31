from django.urls import path

from django_file_upload.confirmation.views import BuyerWiseView

app_name = "confirmation"

urlpatterns = [
    path('buyer-wise/', BuyerWiseView.as_view(), name='buyer_wise'),
]
