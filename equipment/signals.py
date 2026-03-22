from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tool, Machine

@receiver(post_save, sender=Tool)
def sync_tool_compatibility(sender, instance, **kwargs):

    SAFE_FORCE_LIMIT = instance.clamping_force / 0.90
    SAFE_CAPACITY_LIMIT = instance.injection_capacity / 0.85

    MIN_REQUIRED_WIDTH = instance.tool_width / 0.90
    MIN_REQUIRED_HEIGHT = instance.tool_height / 0.90

    compatible_machines = Machine.objects.filter(
        max_clamping_force__gte=SAFE_FORCE_LIMIT,
        max_injection_capacity__gte=SAFE_CAPACITY_LIMIT,
        max_tool_width__gte=MIN_REQUIRED_WIDTH,
        max_tool_height__gte=MIN_REQUIRED_HEIGHT,
        max_tool_thickness__gte=instance.tool_thickness,

        max_tool_thickness__lte=instance.tool_thickness / 0.30,
        number_of_ejector_cores__gte=instance.number_of_ejector_cores,
        max_moving_platen_stroke__gte=instance.moving_platen_stroke,
        max_ejecting_stroke__gte=instance.ejecting_stroke
    )


    current_links = instance.compatible_machines.all()


    outdated_machines = current_links.exclude(id__in=compatible_machines)
    for machine in outdated_machines:
        machine.compatible_tools.remove(instance)


    for machine in compatible_machines:
        machine.compatible_tools.add(instance)




