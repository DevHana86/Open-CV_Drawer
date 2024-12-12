import re
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
from svg_to_gcode import TOLERANCES

TOLERANCES['approximation'] = 0.5

gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)

curves = parse_file("output.svg")

def generate_and_optimize_gcode(curves, output_file):
    previous_coords = None 
    with open(output_file, 'w') as outfile:
        for curve in curves:
            x, y = curve.end.x, curve.end.y
            coords = {'X': x, 'Y': y}
            
            if coords == previous_coords:
                continue
            
            gcode_line = f"G1 X{x:.3f} Y{y:.3f} F1000\n"
            outfile.write(gcode_line)
            
            previous_coords = coords
    
    print(f"G-code 파일 생성 완료: {output_file}")

generate_and_optimize_gcode(curves, "output.gcode")