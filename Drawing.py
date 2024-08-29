import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        canny_edges = cv2.Canny(frame, 50, 150, apertureSize=3)
        inverted_edges = cv2.bitwise_not(canny_edges)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite('canny_image.png', inverted_edges)
            print("이미지가 성공적으로 저장되었습니다.")
            break

        cv2.imshow('Canny Filter', inverted_edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()