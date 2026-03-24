from django.urls import path
from rest_framework.routers import DefaultRouter

import equipment
from equipment import views

app_name = 'equipment'

router = DefaultRouter()
router.register('machines', views.MachineViewSet)
router.register('tools', views.ToolViewSet)


urlpatterns = router.urls