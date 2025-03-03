from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserProfileSerializer
from .permissions import IsAdmin, IsTrader, IsSalesRep, IsCustomer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class TraderDashboardView(generics.GenericAPIView):
    permission_classes = [IsTrader]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Welcome to the Trader Dashboard"}, status=status.HTTP_200_OK)

class SalesDashboardView(generics.GenericAPIView):
    permission_classes = [IsSalesRep]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Welcome to the Sales Dashboard"}, status=status.HTTP_200_OK)

class CustomerDashboardView(generics.GenericAPIView):
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Welcome to the Customer Dashboard"}, status=status.HTTP_200_OK)

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user