from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from django.utils import timezone
from .models import PlayerProfile, Campaign
from .serializers import PlayerProfileSerializer, CampaignSerializer
from .services import match_player_to_campaigns

class PlayerProfileListView(generics.ListAPIView):
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer

class CampaignListView(generics.ListAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

@api_view(['GET'])
def get_client_config(request, player_id):
    try:
        player = PlayerProfile.objects.get(player_id=player_id)
    except PlayerProfile.DoesNotExist:
        return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

    updated_player = match_player_to_campaigns(player)
    serializer = PlayerProfileSerializer(updated_player)
    return Response(serializer.data)
