from django.urls import path

from collection.views import MoviesViews,CollectionView,RequestCounterView

urlpatterns = [
    path('movies/',MoviesViews.as_view()),
    path('collection/',CollectionView.as_view()),
    path('collection/<collection_uuid>/',CollectionView.as_view()),
    path('request-count/',RequestCounterView.as_view()),
    path('request-count/reset/',RequestCounterView.as_view()),
]