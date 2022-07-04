from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password', 'is_active', 'date_joined',
                   'is_staff','is_superuser','last_login')
        
class ShowManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowManager
        fields = '__all__'
class SalespersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesperson
        fields = '__all__'
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(SalespersonSerializer, self).to_representation(instance)
    # def create(self, validated_data):
    #     """
    #     Make necessary modifications as per your requirements
    #     """
    #     print(validated_data)
    #     person_profile = User.create(UserSerializer(), validated_data)
    #     person, created = Salesperson.objects.create(user=person_profile)
    #     return person
    
    
class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'
        
    def to_representation(self, instance):
        self.fields['salesperson'] = SalespersonSerializer(read_only=True)
        return super(ShowSerializer, self).to_representation(instance)




class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class ClerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clerk
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        
    def to_representation(self, instance):
        self.fields['show'] = ShowSerializer(read_only=True)
        return super(TicketSerializer, self).to_representation(instance)
class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        fields = '__all__'
# class SpectatorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Spectator
#         fields = '__all__'