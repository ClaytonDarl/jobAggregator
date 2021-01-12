from django.urls import path, include
from .views import GenericAPIView, PostingDetailsAPIVIew, postingList, postingDetail, postingAPIVIew, PostingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posting', PostingViewSet, basename='posting')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>', include(router.urls)),
    #path('posting/', postingList),
    path('posting/', postingAPIVIew.as_view()),
    path('details/<int:id>/', PostingDetailsAPIVIew.as_view()),
    path('generic/<int:id>/', GenericAPIView.as_view()),
]