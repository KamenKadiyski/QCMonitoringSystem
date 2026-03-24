from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from QCMonitoringSystem.settings import TOOL_TOLERANCE
from .models import Tool, Machine
from django.db.models import Q
def tool_is_compatible(tool, machine, tolerance=TOOL_TOLERANCE):
    return (
        tool.clamping_force >= machine.max_clamping_force * tolerance and
        tool.tool_width >= machine.max_tool_width * tolerance and
        tool.tool_height >= machine.max_tool_height * tolerance and
        tool.tool_thickness >= machine.max_tool_thickness * tolerance and
        tool.moving_platen_stroke >= machine.max_moving_platen_stroke * tolerance and
        tool.injection_capacity >= machine.max_injection_capacity * tolerance and
        tool.ejecting_stroke >= machine.max_ejecting_stroke * tolerance and
        tool.number_of_ejector_cores >= machine.number_of_ejector_cores * tolerance
    )

def compatible_tool_for_machine(machine,tolerance=TOOL_TOLERANCE):
    compatible_tools = Tool.objects.filter(
        Q(clamping_force__gte=machine.max_clamping_force * tolerance) &
        Q(tool_width__gte=machine.max_tool_width * tolerance)&
        Q(tool_height__gte=machine.max_tool_height * tolerance)&
        Q(tool_thickness__lte=machine.max_tool_thickness * tolerance) &
        Q(moving_platen_stroke__gte=machine.max_moving_platen_stroke * tolerance) &
        Q(injection_capacity__gte=machine.max_injection_capacity * tolerance) &
        Q(ejecting_stroke__gte=machine.max_ejecting_stroke * tolerance) &
        Q(number_of_ejector_cores__gte=machine.number_of_ejector_cores * tolerance)
    )
    return compatible_tools

@receiver(post_save, sender=Machine)
def add_compatible_tools_on_machine_create(sender, instance, created, **kwargs):
    if not created:
        return

    compatible_tools = compatible_tool_for_machine(instance)
    if compatible_tools.exists():
        instance.compatible_tools.add(*compatible_tools)


@receiver(m2m_changed, sender=Machine.compatible_tools.through)
def validate_tool_compatibility(sender, instance, action, reverse, pk_set, **kwargs):
    if action!= "pre_add":
        return

    tools = Tool.objects.filter(id__in=pk_set)
    valid = [
        tool.pk for tool in tools if tool_is_compatible(tool, instance)
    ]
    pk_set.clear()
    pk_set.update(valid)



@receiver(post_save, sender=Tool)
def add_tool_to_compatible_machines(sender, instance, created, **kwargs):
    if not created:
        return

    compatible_machines = Machine.objects.filter(
        Q(max_clamping_force__gte=instance.clamping_force / TOOL_TOLERANCE) &
        Q(max_tool_width__gte=instance.tool_width / TOOL_TOLERANCE) &
        Q(max_tool_height__gte=instance.tool_height / TOOL_TOLERANCE) &
        Q(max_tool_thickness__lte=instance.tool_thickness / TOOL_TOLERANCE) &
        Q(max_moving_platen_stroke__gte=instance.moving_platen_stroke / TOOL_TOLERANCE) &
        Q(max_injection_capacity__gte=instance.injection_capacity / TOOL_TOLERANCE) &
        Q(max_ejecting_stroke__gte=instance.ejecting_stroke / TOOL_TOLERANCE) &
        Q(number_of_ejector_cores__gte=instance.number_of_ejector_cores)
    )

    for machine in compatible_machines:
        machine.compatible_tools.add(instance)





