from rest_framework import serializers
from equipment.models import Machine, Tool

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class MachineSerializer(serializers.ModelSerializer):
    compatible_tools = serializers.PrimaryKeyRelatedField(queryset=Tool.objects.all(),
                                                          many=True,
                                                          required=False)
    class Meta:
        model = Machine
        fields = '__all__'

    def create(self,validated_data):
        compatible_tools_data = validated_data.pop('compatible_tools', [])
        machine = Machine.objects.create(**validated_data)
        if compatible_tools_data:
            machine.compatible_tools.add(*compatible_tools_data)

        return machine

    def update(self, instance, validated_data):
        compatible_tools_data = validated_data.pop('compatible_tools', None)
        instance = super().update(instance, validated_data)
        if compatible_tools_data is not None:
            instance.compatible_tools.set(compatible_tools_data)

        return instance







class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'








