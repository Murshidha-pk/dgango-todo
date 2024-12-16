from rest_framework import serializers

from task.models import User,Todo

class UserSerializers(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["id","username","email","phone","password"]

#this django provided for create_user

    def create(self,validated_data):

        return User.objects.create_user(**validated_data)
    

class TodoSerializer(serializers.ModelSerializer):

#show owner in fields

    owner=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Todo

        fields="__all__"

        read_only_fields=["id","created_date","owner"]