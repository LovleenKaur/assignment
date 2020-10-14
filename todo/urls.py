from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo import views

router = DefaultRouter()
router.register('todos', views.TodoViewset)
app_name = 'todo'


urlpatterns = [
    path('', include(router.urls))
]