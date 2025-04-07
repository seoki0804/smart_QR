from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import csv
import uuid
import os
from datetime import datetime

# 모듈 임포트
from modules.qr_generator import generate_qr
from modules.qr_scanner import scan_qr_and_get_item

# 데이터 경로
DATA_FILE = "./database/items.csv"
os.makedirs("./database", exist_ok=True)

# ────────────────────────────────────────
# ① 물품 등록 화면
class RegisterForm(BoxLayout):
    def save_item(self):
        name = self.ids.name_input.text.strip()
        desc = self.ids.desc_input.text.strip()
        qty = self.ids.qty_input.text.strip()

        if not name or not qty.isdigit():
            self.ids.status_label.text = "[오류] 이름과 수량을 확인하세요."
            return

        item_id = str(uuid.uuid4())
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        is_new = not os.path.exists(DATA_FILE)
        with open(DATA_FILE, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["id", "name", "description", "quantity", "created_at"])
            writer.writerow([item_id, name, desc, qty, now])

        generate_qr(item_id, name)

        self.ids.name_input.text = ""
        self.ids.desc_input.text = ""
        self.ids.qty_input.text = ""
        self.ids.status_label.text = f"[저장 완료] {name} 등록 및 QR 생성됨."

# ────────────────────────────────────────
# ② QR 스캔 화면
class ScanForm(BoxLayout):
    def start_scan(self):
        self.ids.status_label.text = "QR 스캔 중... 카메라를 보세요."
        item = scan_qr_and_get_item()

        if item:
            result = f"📦 이름: {item['name']}\n📝 설명: {item['description']}\n📦 수량: {item['quantity']}"
            self.ids.result_label.text = result
            self.ids.status_label.text = "✅ 스캔 성공!"
        else:
            self.ids.result_label.text = ""
            self.ids.status_label.text = "❌ 스캔 실패 또는 물품 없음."

# ────────────────────────────────────────
# ③ 스크린 관리자
class RegisterScreen(Screen):
    pass

class ScanScreen(Screen):
    pass

class SMARTQRApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ScanScreen(name='scan'))
        return sm

if __name__ == '__main__':
    SMARTQRApp().run()