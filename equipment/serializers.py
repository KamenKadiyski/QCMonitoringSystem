from rest_framework import serializers
from equipment.models import Machine

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'
    def validate(self,data):
        tools = data.get('compatible_tools',[])
        if tools:
            max_force = data.get('max_clamping_force')
            max_width = data.get('max_tool_width')
            max_height = data.get('max_tool_height')
            max_thickness = data.get('max_tool_thickness')
            max_moving_platen_stroke = data.get('max_moving_platen_stroke')
            max_injection_capacity = data.get('max_injection_capacity')
            max_ejecting_stroke = data.get('max_ejecting_stroke')
            max_ejector_cores = data.get('number_of_ejector_cores')
            valid_tools = []
            invalid_tools = []

            for tool in tools:
                errors = []
                if  tool.clamping_force > max_force :
                    errors.append(f'Matrix {tool.code} requires {tool.clamping_force}'
                                  f'kN, which exceeds the machine limit ({max_force}kN).')
                if tool.tool_width > max_width:
                    errors.append(f'The dimensions of the tool {tool.code} are larger than the machine plates.')

                if tool.tool_height > max_height:
                    errors.append(f'The dimensions of the tool {tool.code} are larger than the machine plates.')

                if tool.tool_thickness > max_thickness:
                    errors.append(f'The thickness of the tool {tool.code} are larger than the machine plates.')

                if  tool.moving_platen_stroke > max_moving_platen_stroke:
                    errors.append(f'The dimensions of the tool {tool.code} are larger than the machine plates.')

                if tool.injection_capacity > max_injection_capacity:
                    errors.append(f'The injection capacity for {tool.code} is too large for this machine.')

                if tool.ejecting_stroke > max_ejecting_stroke:
                    errors.append(f'The ejecting stroke for {tool.code} is too large for this machine.')

                if tool.number_of_ejector_cores > max_ejector_cores:
                    errors.append(f'The machine and tool {tool.code} must have the same number of ejector cores')
                if errors:
                    invalid_tools.append(tool)
                else:
                    valid_tools.append(tool)
            data['compatible_tools'] = valid_tools
            print(f"Warning: Tools {', '.join(invalid_tools)} were removed due to incompatibility.")
        return data








