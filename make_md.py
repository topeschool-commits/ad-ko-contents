import json
import os

# [작전 설정] 파일 및 폴더 위치 조준
json_file = 'g5_write_namecard.json' # 사령관님이 업로드하신 파일명
output_dir = 'content/posts'        # Hugo의 게시글 보관소

# 폴더가 없으면 즉시 건설
os.makedirs(output_dir, exist_ok=True)

try:
    print(f"⏳ [namecard] 데이터 해독 작전 개시: {json_file} 읽는 중...")
    with open(json_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    records = []
    # phpMyAdmin JSON 구조 자동 대응 및 데이터 추출
    if isinstance(raw_data, list):
        for item in raw_data:
            if isinstance(item, dict) and item.get('type') == 'table':
                records = item.get('data', [])
                break
        if not records and len(raw_data) > 0:
            records = raw_data

    if not records:
        print("❌ 에러: 데이터를 찾을 수 없습니다. JSON 파일의 형식을 확인해 주세요.")
        exit()

    count = 0
    for row in records:
        wr_id = row.get('wr_id')
        if not wr_id: continue

        # 제목 추출 및 특수기호 안전 처리
        title = str(row.get('wr_subject', '제목 없음')).replace('"', '\\"')
        
        # 날짜를 Hugo 규격(ISO 8601)으로 정밀 변환
        date_raw = row.get('wr_datetime', '2024-01-01 00:00:00')
        date = date_raw.replace(' ', 'T') + '+09:00'
        
        # 본문 내용 추출
        content = str(row.get('wr_content', ''))

        # Hugo용 마크다운 전함 건조
        md_content = f"""---
title: "{title}"
date: {date}
draft: false
---

{content}
"""
        # [게시글번호].md 파일로 저장 (SEO 주소 유지 핵심)
        with open(os.path.join(output_dir, f"{wr_id}.md"), 'w', encoding='utf-8') as mf:
            mf.write(md_content)
        count += 1

    print(f"✅ 작전 성공: 총 {count}개의 명함 전함이 {output_dir}/ 폴더에 실전 배치되었습니다!")

except FileNotFoundError:
    print(f"❌ 에러: {json_file} 파일이 사령탑에 없습니다. 업로드 상태를 확인하세요.")
except Exception as e:
    print(f"❌ 알 수 없는 시스템 오류 발생: {e}")