from rest_framework import serializers
from home.models import CardItem

#carditem model serializer
class CardItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardItem
        fields = ['card','product','quantity']