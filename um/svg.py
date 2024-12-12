import subprocess

def png_to_pbm(input_png, output_pbm):
    try:
        # ImageMagick의 `magick convert` 명령을 사용해 PNG를 PBM으로 변환
        subprocess.run(
            f'magick convert "{input_png}" "{output_pbm}"',
            shell=True,
            check=True
        )
        print("PNG를 PBM으로 변환 성공!")
    except subprocess.CalledProcessError as e:
        print(f"PNG를 PBM으로 변환 실패: {e}")

def pbm_to_svg_with_potrace(input_pbm, output_svg):
    try:
        # Potrace를 사용하여 PBM을 SVG로 변환
        subprocess.run(
            f'"D:/potrace-1.16.win64/potrace-1.16.win64/potrace.exe" "{input_pbm}" -s -o "{output_svg}"',
            shell=True,
            check=True
        )
        print("PBM을 SVG로 변환 성공!")
    except subprocess.CalledProcessError as e:
        print(f"PBM을 SVG로 변환 실패: {e}")

def png_to_svg(input_png, output_svg):
    # 1단계: PNG를 PBM으로 변환
    pbm_file = "temp.pbm"  # 임시 PBM 파일 경로
    png_to_pbm(input_png, pbm_file)
    
    # 2단계: PBM을 SVG로 변환
    pbm_to_svg_with_potrace(pbm_file, output_svg)

# 실행 예시
png_to_svg("input.png", "output.svg")
