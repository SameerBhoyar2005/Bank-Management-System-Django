from django.urls import path, include
from rest_framework import routers

from api.views import userViewSet, DipositView, WithdrawView,TransactionView,transfer

router = routers.DefaultRouter()
router.register(r'user',userViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('diposit/<int:id>',DipositView.as_view()),
    path('withdraw/<int:id>',WithdrawView.as_view()),
    path('transactions/<int:id>',TransactionView.as_view()),
    path('transfer',transfer)
    ]