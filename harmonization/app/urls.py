
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name='home'),
    path("docs/", views.docs_view, name='docs'),
    path('upload/', views.upload_view, name='upload'),
    path('preprocess/', views.preprocess_view, name='preprocess'),
    path('downloads/<int:processed_file_id>/', views.download_view, name='download'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)