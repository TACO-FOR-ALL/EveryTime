from rest_framework import serializers
from .models import *

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'region']
        read_only_fields = ['id', 'name', 'region']
    
class OrganizationEmailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationEmail
        fields = ['suffix']
        read_only_fields = ['suffix']