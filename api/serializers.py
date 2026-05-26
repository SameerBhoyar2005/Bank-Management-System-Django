from rest_framework import serializers

from api.models import User,Transactions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        user_id = serializers.ReadOnlyField(source='user.id')
        model = User
        fields = ['name','email','amount']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Transactions
        #fields = '__all__'
        exclude = ['pin']

class DipositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    def vaidate_amount(self,value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be positive')
        return value

class WithdrawSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    pin = serializers.IntegerField()

    def validate_amount (self,value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be positive')
        return value

    def validate_pin (self,value):
        if value < 10000 or value > 99999:
            raise serializers.ValidationError('Pin must be 5 digits')
        return value

class TransferSerializer(serializers.Serializer):
    senderMail = serializers.EmailField()
    receiverMail = serializers.EmailField()
    amount = serializers.IntegerField()
    pin = serializers.IntegerField()
    def validate(self, attrs):
        sender = attrs.get('senderMail')
        receiver = attrs.get('receiverMail')
        amt = attrs.get('amount')
        pin = attrs.get('pin')
        if sender == receiver:
            raise serializers.ValidationError("Sender and receiver both are same")

        if amt <= 0:
            raise serializers.ValidationError("amount must be greater than 0")

        if pin < 10000 or pin > 99999:
            raise serializers.ValidationError("please Enter valid pin")

        return attrs