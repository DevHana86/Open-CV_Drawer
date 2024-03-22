import cv2
import numpy as np

def convert_gcode_to_image(gcode_path, output_image_path, image_size=(500, 500)):
    # 이미지 생성 (흰색 바탕)
    image = 255 * np.ones(image_size, dtype=np.uint8)

    # G코드 파일 열기
    with open(gcode_path, 'r') as f:
        # 각 라인에 대해 처리
        for line in f:
            if line.startswith('G01'):
                # G01 명령이 있는 경우 X, Y 좌표 추출
                tokens = line.split()
                x = float(tokens[1][1:])  # 'X' 다음 문자부터 좌표값
                y = float(tokens[2][1:])  # 'Y' 다음 문자부터 좌표값
                
                # 이미지 좌표로 변환
                img_x = int((x / 100) * image_size[1])  # 100x100mm 이미지를 가정
                img_y = image_size[0] - int((y / 100) * image_size[0])  # 이미지를 상하 반전하여 계산

                # 변환된 좌표에 점 그리기
                cv2.circle(image, (img_x, img_y), radius=1, color=(0, 0, 0), thickness=-1)

    # 이미지 저장
    cv2.imwrite(output_image_path, image)

# G코드 파일을 이미지로 변환
convert_gcode_to_image('output_gcode.gcode', 'output_image.png')