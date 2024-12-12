import cv2

def apply_canny_to_image(image_path, output_path):
    # 이미지 읽기
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    if image is None:
        print(f"이미지를 불러올 수 없습니다: {image_path}")
        return

    # Canny 에지 검출
    canny_edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # 반전 처리 (선택 사항)
    inverted_edges = cv2.bitwise_not(canny_edges)

    # Canny 필터 적용된 이미지 저장
    cv2.imwrite(output_path, inverted_edges)
    print(f"Canny 에지가 적용된 이미지가 저장되었습니다: {output_path}")

# 사용 예시
apply_canny_to_image("input.png", "input.png")
