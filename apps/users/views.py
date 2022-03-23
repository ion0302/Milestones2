from datetime import datetime, timezone, timedelta

from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.logs.models import Log
from apps.users.serializers import UserSerializer, UserListSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
            username=serializer.validated_data['email'],
            is_superuser=False,
            is_staff=False
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(data=UserSerializer(user).data)


class UserListViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    # @action(detail=False, methods=['GEt'], url_path='my-logs')
    # def my_logs(self, request, *args, **kwargs):
    #     user = self.request.user
    #     last_month = datetime.now(tz=timezone.utc) - timedelta(days=30)
    #     logs = Log.objects.filter(user=user).filter(stop__gte=last_month)
    #     log_sum = 0
    #     for log in logs:
    #         log_time = log.stop - log.start
    #         log_sum += log_time.total_seconds()/60

