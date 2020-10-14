from rest_framework import serializers
from core.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for todo object"""

    class Meta:
        model = Todo
        fields = ('id', 'task', 'completed', 'created_at')
        read_only_fields = ('id',)