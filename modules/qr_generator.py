import qrcode
import os

# QR코드 이미지 저장 경로
QR_DIR = "./qr_codes"

# 폴더가 없으면 자동 생성
os.makedirs(QR_DIR, exist_ok=True)

def generate_qr(item_id, item_name=None):
    """
    고유 item_id를 QR코드로 만들어 이미지로 저장

    Args:
        item_id (str): UUID 또는 고유값
        item_name (str): 물품 이름 (파일 이름에 추가할 수 있음)
    """
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(item_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')

    # 파일 이름 구성
    if item_name:
        safe_name = item_name.replace(" ", "_")
        filename = f"{safe_name}_{item_id[:6]}.png"
    else:
        filename = f"{item_id}.png"

    filepath = os.path.join(QR_DIR, filename)
    img.save(filepath)

    print(f"[QR 저장 완료] {filepath}")
    return filepath