from rest_framework import generics
from rest_framework.response import Response
from tasks.serializer import (
    RegisterSerializer, TaskSerializer, UpdateTaskSerializer
    )
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from tasks.models import Task, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError


# Register API
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


# only client can create
class TaskCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        if self.request.user.role == 'Client':
            serializer.save(create_by=self.request.user)
        else:
            raise ValidationError(
                {'error': 'You are not authorized to create tasks.'})


class TaskUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateTaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(id=self.kwargs['pk'])
        return queryset

    def perform_update(self, serializer):
        if self.request.user.role == 'Manager':
            user = CustomUser.objects.filter(
                username=self.request.data['assigned_to'],
                role="Employee")
            if user:
                serializer.save(assigned_to=user[0].id)
            else:
                raise ValidationError({"Error": "user is not valid"})
        else:
            raise ValidationError(
                {'error': 'You are not authorized to assign tasks.'})


class TaskDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(id=self.kwargs['pk'])
        return queryset

    def perform_destroy(self, instance):
        if self.request.user.role == 'Manager':
            instance.delete()
            raise ValidationError(
                {'message': 'Delete Sucessfully.'},
                status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(
                {'error': 'You are not authorized to delete tasks.'})


class TaskCompleteView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(id=self.kwargs['pk'])
        return queryset

    def perform_update(self, serializer):
        if self.request.user.role == 'Employee':
            user = Task.objects.filter(assigned_to=self.request.user, status='pending')
            if user:
                serializer.save(status='Complete')
        else:
            raise ValidationError(
                {'error': 'You are not authorized to complete tasks.'})


# logout api
class BlacklistRefreshView(generics.CreateAPIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")
