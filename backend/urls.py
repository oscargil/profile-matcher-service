from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path
from matcher.views import get_client_config, PlayerProfileListView, CampaignListView

schema_view = get_schema_view(
   openapi.Info(
      title="Profile Matcher API",
      default_version='v1',
      description="API documentation for the Profile Matcher Service",
      contact=openapi.Contact(email="ogilsot@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_client_config/<str:player_id>/', get_client_config, name='get_client_config'),
    path('players/', PlayerProfileListView.as_view(), name='player-list'),
    path('campaigns/', CampaignListView.as_view(), name='campaign-list'),
]

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
