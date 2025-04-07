



# SMART_QR 📦📲

🧑‍💻  팀원
| 이진규| 안형석| 최명희| 정민영 |
프로젝트명: SMART_QR
 
## ➖ 프로젝트 기간
- 2025년 03월 12일 시작

  
**스마트 QR 기반 물품 재고 관리 앱 (안드로이드용)**  
파이썬 + Kivy로 제작된 이 앱은 물품 등록, QR코드 생성/스캔, 재고 관리 및 엑셀 보고서 출력 기능을 제공합니다.

---

## 🔧 주요 기능

| 기능 | 설명 |
|------|------|
| 📥 물품 등록 | 물품명, 설명, 초기 수량 입력 → QR 자동 생성 |
| 📷 QR코드 스캔 | 카메라로 QR코드 인식 후 해당 물품 정보 불러오기 |
| ✍️ 수급/소모/청구 입력 예정 | 스캔된 물품에 대해 입출고 정보 기록 예정 |
| 📊 엑셀 보고서 생성 예정 | 재고 현황, 청구서, 사용 보고서 출력 예정 |

---

## 🛠️ 기술 스택

- **Python 3.x**
- **Kivy** – Android 앱 UI 프레임워크
- **Buildozer** – Android `.apk` 빌드 툴
- **OpenCV + pyzbar** – QR 인식 (카메라 기반)
- **qrcode** – QR코드 이미지 생성
- **pandas + openpyxl** – 엑셀 저장 및 보고서 출력

---

## 📁 프로젝트 구조

SMART_QR/
├── main.py                        # 앱 진입점
├── itemform.kv                    # 물품 등록 UI
├── scanform.kv                    # QR 스캔 UI
│
├── modules/                       # 기능별 모듈
│   ├── qr_generator.py            # QR 이미지 생성
│   ├── qr_scanner.py              # 카메라로 QR 인식
│   └── (추가 예정) transaction_manager.py
│
├── database/                      # 데이터 저장소
│   ├── items.csv                  # 물품 정보
│   └── (추가 예정) transactions.xlsx
│
├── qr_codes/                      # 생성된 QR 이미지 저장
├── reports/                       # 보고서 (.xlsx) 저장 예정
├── assets/                        # 앱 리소스 (로고, 폰트 등)
└── buildozer.spec                 # Android APK 빌드 설정

---

## ✅ 설치 및 실행 방법

### 1. 환경 설정

```bash
pip install -r requirements.txt

또는 수동 설치:

pip install kivy qrcode opencv-python pyzbar pandas openpyxl

	📦 macOS 사용자는 brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf gstreamer 필요

2. 앱 실행

python main.py

3. Android 빌드

buildozer init
buildozer -v android debug

	⚠️ APK 빌드는 Ubuntu에서만 가능.
macOS는 Docker 또는 가상머신(Ubuntu) 필요

🔮 향후 계획
	•	수급/소모/청구량 기록 입력 기능
	•	transactions.xlsx 엑셀 저장
	•	다양한 보고서 템플릿 생성 기능
	•	앱 테마 및 사용자 UI 개선


