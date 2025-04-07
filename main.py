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
from modules.transaction_manager import append_transaction
from modules.report_exporter import export_reports

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
# ② QR 스캔 및 거래 기록 화면
class ScanForm(BoxLayout):
    scanned_item = None  # 스캔된 물품 정보 저장

    def start_scan(self):
        self.ids.status_label.text = "QR 스캔 중... 카메라를 보세요."
        item = scan_qr_and_get_item()

        if item:
            self.scanned_item = item
            result = f"📦 이름: {item['name']}\n📝 설명: {item['description']}\n📦 수량: {item['quantity']}"
            self.ids.result_label.text = result
            self.ids.status_label.text = "✅ 스캔 성공!"
        else:
            self.scanned_item = None
            self.ids.result_label.text = ""
            self.ids.status_label.text = "❌ 스캔 실패 또는 물품 없음."

    def save_transaction(self):
        if not self.scanned_item:
            self.ids.status_label.text = "[오류] 먼저 QR을 스캔해주세요."
            return

        try:
            intake = int(self.ids.intake_input.text) if self.ids.intake_input.text else 0
            usage = int(self.ids.usage_input.text) if self.ids.usage_input.text else 0
            request = int(self.ids.request_input.text) if self.ids.request_input.text else 0
            memo = self.ids.memo_input.text.strip()
        except ValueError:
            self.ids.status_label.text = "[오류] 수량 입력이 잘못되었습니다."
            return

        append_transaction(
            item_id=self.scanned_item["id"],
            item_name=self.scanned_item["name"],
            intake=intake,
            usage=usage,
            request=request,
            memo=memo
        )

        self.ids.intake_input.text = ""
        self.ids.usage_input.text = ""
        self.ids.request_input.text = ""
        self.ids.memo_input.text = ""
        self.ids.status_label.text = "💾 거래 내역 저장 완료!"

    def generate_reports(self):
        export_reports()
        self.ids.status_label.text = "📊 보고서가 생성되었습니다! reports 폴더를 확인하세요."

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