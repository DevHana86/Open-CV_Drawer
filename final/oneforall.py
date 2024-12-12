import cv2
from PIL import Image
import subprocess
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode import TOLERANCES

TOLERANCES['approximation'] = 0.5

def capture_photo(output_filename):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("카메라 안 열림")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임 못 읽음 ㅅㄱ")
            break

        height, width = frame.shape[:2]
        min_dim = min(width, height)
        center_x, center_y = width // 2, height // 2
        start_x = center_x - min_dim // 2
        start_y = center_y - min_dim // 2
        square_frame = frame[start_y:start_y + min_dim, start_x:start_x + min_dim]

        cv2.imshow('저장하려면 s, 그만 두려면 q 클릭ㄱㄱ', square_frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            cv2.imwrite(output_filename, square_frame)
            print(f"이미지가 저장됨: {output_filename}")
            break
        elif key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def apply_canny(image_path, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"이미지를 불러짐: {image_path}")
        return

    canny_edges = cv2.Canny(image, 50, 150, apertureSize=3)
    inverted_edges = cv2.bitwise_not(canny_edges)
    cv2.imwrite(output_path, inverted_edges)
    print(f"Canny 변환 이미지 저장됨: {output_path}")

def resize_image(image_path, output_size=(600, 600)):
    img = Image.open(image_path)
    img.thumbnail(output_size, Image.LANCZOS)
    img.save(image_path)
    print(f"이미지 크기 제한 후 저장됨: {image_path}")

def png_to_pbm(input_png, output_pbm):
    try:
        subprocess.run(
            f'magick "{input_png}" "{output_pbm}"',
            shell=True,
            check=True
        )
        print("PNG를 PBM으로 변환 성공!")
    except subprocess.CalledProcessError as e:
        print(f"PNG를 PBM으로 변환 실패: {e}")

def pbm_to_svg_with_potrace(input_pbm, output_svg):
    try:
        subprocess.run(
            f'"D:/potrace-1.16.win64/potrace-1.16.win64/potrace.exe" "{input_pbm}" -s -o "{output_svg}"',
            shell=True,
            check=True
        )
        print("PBM을 SVG로 변환 성공!")
    except subprocess.CalledProcessError as e:
        print(f"PBM을 SVG로 변환 실패: {e}")

def png_to_svg(input_png, output_svg):
    pbm_file = "../final/temp.pbm"
    png_to_pbm(input_png, pbm_file)
    pbm_to_svg_with_potrace(pbm_file, output_svg)

def generate_and_optimize_gcode(svg_file, output_file):
    curves = parse_file(svg_file)
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

def transform_gcode(input_file, output_file):
    with open(input_file, 'r') as file:
        gcode_lines = file.readlines()

    transformed_gcode = []
    previous_x, previous_y = None, None

    for i, line in enumerate(gcode_lines):
        line = line.strip()
        if line.startswith("G1"):
            x_val = y_val = None
            parts = line.split()
            for part in parts:
                if part.startswith("X"):
                    x_val = float(part[1:])
                elif part.startswith("Y"):
                    y_val = float(part[1:])

            if previous_x is not None and previous_y is not None:
                if (x_val is not None and abs(x_val - previous_x) >= 100) or \
                   (y_val is not None and abs(y_val - previous_y) >= 100):
                    transformed_gcode.append("G1 Z0")
                    transformed_gcode.append(line)
                    next_line = gcode_lines[i + 1].strip() if i + 1 < len(gcode_lines) else None
                    if next_line:
                        transformed_gcode.append("G1 Z-6")
                        transformed_gcode.append(next_line)
                    previous_x = x_val if x_val is not None else previous_x
                    previous_y = y_val if y_val is not None else previous_y
                    continue

            previous_x = x_val if x_val is not None else previous_x
            previous_y = y_val if y_val is not None else previous_y
        transformed_gcode.append(line)

    with open(output_file, 'w') as file:
        for line in transformed_gcode:
            file.write(line + '\n')

    print(f"G-code 변환 완료: {output_file}")

if __name__ == "__main__":
    captured_filename = "../final/canny.png"
    canny_filename = "../final/canny.png"
    svg_filename = "../final/output.svg"
    gcode_filename = "../final/output.gcode"
    transformed_gcode_filename = "../final/output.gcode"

    capture_photo(captured_filename)
    apply_canny(captured_filename, canny_filename)
    resize_image(canny_filename)
    png_to_svg(canny_filename, svg_filename)
    generate_and_optimize_gcode(svg_filename, gcode_filename)
    transform_gcode(gcode_filename, transformed_gcode_filename)