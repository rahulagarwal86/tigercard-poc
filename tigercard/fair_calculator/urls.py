from django.conf.urls import url
from .views import FairCalculatorAPI

urlpatterns = [

    url(r'^calculate-fare/$', FairCalculatorAPI.as_view(), name='calculate-fare'),
]
