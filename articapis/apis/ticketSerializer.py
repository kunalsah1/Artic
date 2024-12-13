from rest_framework import serializers
from .models import Ticket, Building, Floor

class TicketSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building_id.name', read_only=True)
    floor_name = serializers.CharField(source='floor_id.name', read_only=True)
    unit_name = serializers.CharField(source='unit_id.name', read_only=True)
    category_name = serializers.CharField(source='category_id.name', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category_id.name', read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'


