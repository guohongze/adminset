#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.conf.urls import url, include
from .models import test
#from rest_framework import permissions


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#############################################

class testSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = test
        fields = ('url','username', 'password')
        #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class testViewSet(viewsets.ModelViewSet):
    queryset = test.objects.all()
    serializer_class = testSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'test', testViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]