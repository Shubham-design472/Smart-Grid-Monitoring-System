from rest_framework import serializers
from .models import GridData

class GridDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridData
        fields = '__all__'

