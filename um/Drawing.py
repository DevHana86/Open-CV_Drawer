import cv2

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width = frame.shape[:2]
        min_dim = min(height, width)

        # 중앙 정사각형 좌표 계산
        center_x, center_y = width // 2, height // 2
        start_x = center_x - min_dim // 2
        start_y = center_y - min_dim // 2
        cropped_frame = frame[start_y:start_y + min_dim, start_x:start_x + min_dim]

        # Canny 에지 검출 및 반전 처리
        canny_edges = cv2.Canny(cropped_frame, 50, 150, apertureSize=3)
        inverted_edges = cv2.bitwise_not(canny_edges)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            # 정사각형 이미지만 저장
            cv2.imwrite('input.png', inverted_edges)
            print("정사각형 이미지가 성공적으로 저장되었습니다.")
            break

        cv2.imshow('Canny Filter', inverted_edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()