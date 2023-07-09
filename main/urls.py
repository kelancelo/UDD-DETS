from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "main"
urlpatterns = [
    path('logout', views.custom_logout, name="custom_logout"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.index, name="index"),
    path("<int:round_id>/<int:participant_id>/check", views.check_if_participant_has_been_scored),
    path("save", views.save_scores, name="save_scores"),
    path("<int:round_id>/participants", views.get_participants),
    path("<int:round_id>/<int:participant_id>/extra-data", views.get_extra_participant_data),
    path("<int:round_id>/criteria", views.get_criteria),
    path("stats", views.get_stats, name="stats"),
    path("last_event", views.get_last_event_info),
    path("download", views.download_last_event_info)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)