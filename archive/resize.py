from PIL import Image

# 이미지 파일 열기
img = Image.open('input.png')

img.thumbnail((600, 600), Image.LANCZOS)

img.save('input.png')

print('이미지가 성공적으로 저장되었습니다.: input.png')