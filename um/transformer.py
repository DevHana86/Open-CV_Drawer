# G-code 파일 읽기
with open('output.gcode', 'r') as file:
    gcode_lines = file.readlines()

# 초기화
transformed_gcode = []
previous_x, previous_y = None, None

for i, line in enumerate(gcode_lines):
    # G-code 줄에서 X와 Y 좌표 추출
    line = line.strip()
    if line.startswith("G1"):
        x_val = y_val = None
        # X와 Y 값을 추출합니다
        parts = line.split()
        for part in parts:
            if part.startswith("X"):
                x_val = float(part[1:])
            elif part.startswith("Y"):
                y_val = float(part[1:])

        # X나 Y 좌표의 큰 폭 변화를 체크 (100 이상의 차이)
        if previous_x is not None and previous_y is not None:
            if (x_val is not None and abs(x_val - previous_x) >= 100) or \
               (y_val is not None and abs(y_val - previous_y) >= 100):
                
                # 큰 변화가 있을 경우 `off`, 다음 줄 G-code, 그 다음에 `on` 추가
                transformed_gcode.append("off")  # `off`를 먼저 추가
                transformed_gcode.append(line)   # 큰 변화가 발생한 G-code 줄 추가
                
                # `on`을 그 다음 줄에 추가하기 위해 다음 줄 가져오기
                next_line = gcode_lines[i + 1].strip() if i + 1 < len(gcode_lines) else None
                if next_line:
                    transformed_gcode.append("on")        # 그다음에 `on` 추가
                    transformed_gcode.append(next_line)   # 다음 G-code 줄 추가
                # 갱신 후 continue로 다음 줄 처리
                previous_x = x_val if x_val is not None else previous_x
                previous_y = y_val if y_val is not None else previous_y
                continue

        # 큰 변화가 없는 경우, 단순히 값을 갱신하고 줄 추가
        previous_x = x_val if x_val is not None else previous_x
        previous_y = y_val if y_val is not None else previous_y
        transformed_gcode.append(line)

# 변환된 G-code 파일 저장
with open('transformed_output.gcode', 'w') as file:
    for line in transformed_gcode:
        file.write(line + '\n')
