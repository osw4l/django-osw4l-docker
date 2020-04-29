from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^devices/$', views.DeviceList.as_view(), name='device_list'),
    url(r'^devices/(?P<pk>[0-9]+)/$', views.DeviceDetail.as_view(),
        name='device_detail'),
    url(r'^send/$', views.FCMList.as_view(), name='fcm_send'),
)
