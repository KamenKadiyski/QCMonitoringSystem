from django.apps import AppConfig


class EquipmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.equipment'


    def ready(self):
        import backend.equipment.signals
