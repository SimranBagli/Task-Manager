from tasks.models import CustomUser, Task
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status')


class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('assigned_to', )
