from django.urls import path
from . import views

urlpatterns = [
  path('reports/totalweight/', views.ReportTotalWeightByPlanetView.as_view(), name='ReportTotalWeightByPlanet'),
]