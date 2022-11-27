from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.landing, name="landingPage"),
    path('home/', views.home, name='homePage'),
    path('docs/', views.docs, name='docPage')
    # path('history/', views.history, name='historyPage'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
