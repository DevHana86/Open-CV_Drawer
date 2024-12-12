import cv2

def capture_photo(output_filename):
    # 카메라 초기화 (0번 카메라)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        # 이미지의 가로, 세로 크기 추출
        height, width = frame.shape[:2]
        
        # 가로, 세로 중 작은 값으로 정사각형 영역 설정
        min_dim = min(width, height)
        
        # 중앙을 기준으로 정사각형 자르기
        center_x, center_y = width // 2, height // 2
        start_x = center_x - min_dim // 2
        start_y = center_y - min_dim // 2
        cropped_frame = frame[start_y:start_y + min_dim, start_x:start_x + min_dim]

        # 프레임을 윈도우에 표시
        cv2.imshow('Press "s" to Save or "q" to Quit', cropped_frame)

        # 키 입력 대기 (1ms) - 's'를 누르면 사진 저장, 'q'를 누르면 종료
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            # 정사각형으로 자른 이미지 저장
            cv2.imwrite(output_filename, cropped_frame)
            print(f"이미지가 성공적으로 저장되었습니다: {output_filename}")
            break
        elif key & 0xFF == ord('q'):
            break

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

# 사용 예시
capture_photo('input.png')
