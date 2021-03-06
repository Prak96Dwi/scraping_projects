""" core/serializer.py """
from rest_framework import serializers


class ContentTextSerializer(serializers.Serializer): # pylint: disable=abstract-method
    """
    This content serializer is used to serializer
    name and detail of a person whose information we want to search.

    """
    name = serializers.CharField(max_length=100)
    detail = serializers.CharField(max_length=300)
