from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView
from django.http.response import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.models import Site
from django.conf import settings



# labrary_site_domain = Site.objects.get(name="labrary-domain")

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_CALLBACK_URL
    client_class = OAuth2Client

def callback(request):
    return HttpResponse(request.GET.get('code'))

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected(request):
    return Response(data={ "username": request.user.username })
