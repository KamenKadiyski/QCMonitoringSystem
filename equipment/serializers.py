from rest_framework import serializers
from equipment.models import Machine, Tool

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class MachineSerializer(serializers.ModelSerializer):
    compatible_tools = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tool.objects.all(),
        required=False
    )
    class Meta:
        model = Machine
        fields = '__all__'
    def validate(self,data):
        tools = data.get('compatible_tools',[])
        if not tools:
            return data
        SAFE_FORCE_MARGIN = 0.90  # Безопасна сила на натиска (kN)
        SAFE_INJECTION_MARGIN = 0.85  # Безопасен обем на инжетираният материал (cm3)
        SAFE_DIMENSION_MARGIN = 0.98  # Максимален безопасен допуск за размери (mm)


        if tools:
            max_force = data.get('max_clamping_force') * SAFE_FORCE_MARGIN
            max_width = data.get('max_tool_width') * SAFE_DIMENSION_MARGIN
            max_height = data.get('max_tool_height') * SAFE_DIMENSION_MARGIN
            max_thickness = data.get('max_tool_thickness')
            max_moving_platen_stroke = data.get('max_moving_platen_stroke')
            max_injection_capacity = data.get('max_injection_capacity') * SAFE_INJECTION_MARGIN
            max_ejecting_stroke = data.get('max_ejecting_stroke')
            max_ejector_cores = data.get('number_of_ejector_cores')
            min_thickness_limit = data.get('max_tool_thickness') * 0.30
            valid_tools = []
            invalid_tools = []

            for tool in tools:
                errors = []
                if  tool.clamping_force > max_force :
                    errors.append(f'Matrix {tool.code} requires {tool.clamping_force}'
                                  f'kN, which exceeds the machine safe limit ({max_force}kN).')
                if tool.tool_width > max_width:
                    errors.append("Dimensions exceed tie-bar spacing or plate clearance")

                if tool.tool_height > max_height:
                    errors.append("Dimensions exceed tie-bar spacing or plate clearance")

                if tool.tool_thickness > max_thickness:
                    errors.append("Tool thickness exceeds maximum platen daylight")

                if tool.tool_thickness < min_thickness_limit:
                    errors.append(
                        f"Tool thickness {tool.tool_thickness}mm is below machine minimum ({min_thickness_limit}mm)")

                if  tool.moving_platen_stroke > max_moving_platen_stroke:
                    errors.append(f'The dimensions of the tool {tool.code} are larger than the machine plates.')

                if tool.injection_capacity > max_injection_capacity:
                    errors.append(f"Injection volume: {tool.injection_capacity}cm3 > safe limit {max_injection_capacity}cm3")

                if tool.ejecting_stroke > max_ejecting_stroke:
                    errors.append("Ejector stroke is too long for this machine")

                if tool.number_of_ejector_cores > max_ejector_cores:
                    errors.append(f"Requires {tool.number_of_ejector_cores} cores, machine has {max_ejector_cores}")
                if errors:
                    invalid_tools.append(f"{tool.code}: ({' | '.join(errors)})")
                else:
                    valid_tools.append(tool)

            if invalid_tools:
                print("\nWARNING: Incompatible tools removed")
                for msg in invalid_tools:
                    print(f"REJECTED: {msg}")

            data['compatible_tools'] = valid_tools

        return data






class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'








