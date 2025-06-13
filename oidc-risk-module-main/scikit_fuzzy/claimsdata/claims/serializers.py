from rest_framework import serializers
from .models import ClaimTableEducation, ClaimTableOSP, Transaction

class ClaimTableEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimTableEducation
        fields = ['id', 'claim_designation', 'impact', 'gdpr_compliance']

class ClaimTableOSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimTableOSP
        fields = ['id', 'claim_designation', 'impact', 'gdpr_compliance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'transaction']
