import cv2
from pyzbar.pyzbar import decode
import csv

DATA_FILE = "./database/items.csv"

def scan_qr_and_get_item():
    cap = cv2.VideoCapture(0)  # 기본 카메라 사용

    print("[INFO] 카메라를 시작합니다. QR코드를 보여주세요.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] 카메라 입력 없음.")
            break

        # QR코드 인식
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            item_id = obj.data.decode("utf-8")
            print(f"[INFO] QR 인식됨! ID: {item_id}")
            cap.release()
            cv2.destroyAllWindows()

            # 해당 ID로 물품 정보 조회
            item_info = get_item_by_id(item_id)
            return item_info

        cv2.imshow("QR 코드 스캔 중 - q 누르면 종료", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

def get_item_by_id(item_id):
    try:
        with open(DATA_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == item_id:
                    return row
    except FileNotFoundError:
        print("[ERROR] 데이터 파일이 없습니다.")
    return None