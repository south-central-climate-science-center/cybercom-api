__author__ = 'mstacy'

from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    content = serializers.CharField(max_length=200)
    timestamp = serializers.DateTimeField()
    #args = serializers.Ed
