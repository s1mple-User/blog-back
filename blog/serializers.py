from rest_framework import serializers
from .models import IBlog, IAuthor
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)

        if user is None:
           raise PermissionDenied("Incorrect email or password")


        return super().validate(attrs)

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAuthor
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = IAuthor.objects.create(
            email=validated_data['email'],
            name=validated_data.get('name', ''),
            image = validated_data.get('image'),
            bio=validated_data.get('bio', '') 
        )
        if password:
         user.is_active = True
         user.set_password(password)
         user.save()
        return user



class IAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAuthor
        fields = ['id', 'email', 'name', 'image', 'bio']



class IBlogSerializer(serializers.ModelSerializer):
    author = IAuthorSerializer(read_only=True)

    class Meta:
        model = IBlog
        fields = [
            'id',
            'title',
            'description',
            'image',
            'createdAt',
            'content',
            'slug',
            'author'
        ]
        read_only_fields = ['author']
    

class IBlogSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = IBlog
        fields = [
            'id',
            'title',
            'image',
            'createdAt',
            'slug',
        ]
    