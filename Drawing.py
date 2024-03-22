import cv2
import numpy as np

def apply_canny_filter(image):
    # 이미지의 중간값 계산
    med_val = np.median(image)

    # 하위 임계값을 중간값의 70%로 설정
    lower = int(max(0, 0.7 * med_val))

    # 상위 임계값을 중간값의 130%로 설정
    upper = int(min(255, 1.3 * med_val))

    # 가우시안 블러 적용
    blurred = cv2.GaussianBlur(image, (3, 3), 0)

    # 캐니 엣지 검출
    edges = cv2.Canny(blurred, lower, upper)

    return edges

def convert_to_gcode(image_path, output_path, feed_rate=200, laser_power=255):
    # G코드 파일을 쓰기 모드로 열기
    with open(output_path, 'w') as f:
        # 이미지 불러오기
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # 이미지 크기 구하기
        height, width = image.shape
        
        # 이미지의 유효 픽셀 영역 계산
        valid_pixels = np.where(image == 255)
        
        # 픽셀 영역을 기반으로 G코드 생성
        for y, x in zip(valid_pixels[0], valid_pixels[1]):
            # G코드로 변환된 X 및 Y 좌표 계산
            gcode_x = (x / width) * 100  # 이미지를 100x100mm 영역으로 가정
            gcode_y = ((height - y) / height) * 100  # 이미지를 뒤집어서 Y 좌표 계산
            
            # G01 명령으로 이동
            gcode_line = f'G01 X{gcode_x:.2f} Y{gcode_y:.2f} F{feed_rate} S{laser_power}\n'
            f.write(gcode_line)

def main():
    # 웹캠 캡처 객체 생성
    cap = cv2.VideoCapture(0)

    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            break

        # 캐니 필터 적용
        canny_edges = apply_canny_filter(frame)

        # 's' 키를 누르면 이미지를 PNG 파일로 저장하고 G코드로 변환
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite('canny_image.png', canny_edges)
            print("이미지가 성공적으로 저장되었습니다.")
            convert_to_gcode('canny_image.png', 'output_gcode.gcode')
            print("G코드가 생성되었습니다.")
            break

        # 캐니 필터 적용된 이미지 출력
        cv2.imshow('Canny Filter', canny_edges)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 종료
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()