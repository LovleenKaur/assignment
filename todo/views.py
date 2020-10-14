from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Todo
from todo import serializers


class TodoViewset(viewsets.ModelViewSet):
    """Manage tods in database"""
    serializer_class = serializers.TodoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Todo.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new todo"""
        serializer.save(user=self.request.user)