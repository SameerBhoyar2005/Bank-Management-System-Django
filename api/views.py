from typing import Any

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User,Transactions
from api.serializers import (UserSerializer, DipositSerializer, WithdrawSerializer,TransactionSerializer,
                             TransferSerializer)


class userViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DipositView(APIView):

    def post(self,request,id):
        serializer = DipositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({
                    "message": "User does not exist"
                },status=status.HTTP_404_NOT_FOUND)
            user.amount += amount
            user.save()

            Transactions.objects.create(
                account = user,
                transaction_type = 'DEPOSIT',
                amount = amount
            )

            return Response({"message" : "Successfully Diposited",
                             "new balance": user.amount},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawView(APIView):

    def post(self,request,id):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            pin = serializer.validated_data['pin']
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({"Message" : "User does not exists. Please create Account first"},
                                status=status.HTTP_404_NOT_FOUND)

            if pin == user.pin and user.amount >= amount:
                user.amount -= amount
                user.save()
                Transactions.objects.create(
                    account=user,
                    transaction_type='WITHDRAW',
                    amount=amount
                )

            return Response({"Message" : "Amount Withdrawed SuccessFully",
                             "New Amount": user.amount},
                            status=status.HTTP_200_OK)
        return Response({"Message": "Please Check Credentials"},
                        status=status.HTTP_400_BAD_REQUEST)


class TransactionView(APIView):

    def get(self,request,id):

        try:
            account = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'Message':'User Not Exists'},
                            status=status.HTTP_404_NOT_FOUND)
        transactions = account.transactions.all()

        serializer = TransactionSerializer(transactions,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['PUT'])
def transfer(request):
    serializer = TransferSerializer(data= request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        sender_email =data['senderMail']
        receiver_email = data['receiverMail']
        amount = data['amount']
        pin = data['pin']
        try:
            sender = User.objects.get(email = sender_email)
            receiver = User.objects.get(email = receiver_email)
        except User.DoesNotExist:
            return Response({
                'message' : 'sender or receiver does not exists'
            }, status= status.HTTP_404_NOT_FOUND)

        if sender.pin == pin :
            if amount <= sender.amount:
                sender.amount -= amount
                receiver.amount += amount
                sender.save()
                receiver.save()
                Transactions.objects.create(
                    account=sender,
                    transaction_type='TRANSFER',
                    amount=amount
                )
                Transactions.objects.create(
                    account=receiver,
                    transaction_type='TRANSFER',
                    amount=amount
                )
                return Response({
                    'message': 'TRANSFERRED SUCCESSFULLY'
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'INSUFFICIENT BALANCE'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'message': 'INCORRECT PIN'
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        'message': 'INVALID CREDENTIALS'
    }, status=status.HTTP_400_BAD_REQUEST)




