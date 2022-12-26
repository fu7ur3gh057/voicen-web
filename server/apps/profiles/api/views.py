import uuid

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.profiles.api.serializers import ProfileSerializer, UpdateProfileSerializer
from apps.profiles.exceptions import ProfileNotFound, NotYourProfile
from apps.profiles.models import Profile
# from apps.profiles.renderers import ProfileJSONRenderer

# ALL METHODS ARE AUTHENTICATED


# GET PROFILE
class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [ProfileJSONRenderer]

    def get(self, request: Request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


# UPDATE PROFILE
class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def put(self, request):
        try:
            pass
        except Profile.DoesNotExist:
            raise ProfileNotFound
        data = request.data
        serializer = UpdateProfileSerializer(instance=request.user.profile, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# UPDATE API TOKEN
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_api_token(request: Request):
    user = request.user
    new_token = uuid.uuid4()
    user.profile.api_token = new_token
    user.save()
    return Response({"api_token": f'{new_token}'})
