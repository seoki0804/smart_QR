import os
import pandas as pd
from datetime import datetime

TRANSACTION_FILE = "./database/transactions.xlsx"
REPORT_DIR = "./reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def export_reports():
    if not os.path.exists(TRANSACTION_FILE):
        print("[ERROR] 거래 기록이 존재하지 않습니다.")
        return

    df = pd.read_excel(TRANSACTION_FILE)

    # 날짜 문자열 생성
    now_str = datetime.now().strftime("%Y-%m")

    # 📄 1. 청구서
    invoice = df[df["청구량"] > 0]
    invoice_file = os.path.join(REPORT_DIR, f"청구서_{now_str}.xlsx")
    invoice.to_excel(invoice_file, index=False)

    # 📄 2. 재고 현황 (물품별 총 수급 - 소모)
    stock_summary = (
        df.groupby("물품명")[["수급량", "소모량"]]
        .sum()
        .assign(재고=lambda x: x["수급량"] - x["소모량"])
        .reset_index()
    )
    stock_file = os.path.join(REPORT_DIR, f"재고현황_{now_str}.xlsx")
    stock_summary.to_excel(stock_file, index=False)

    # 📄 3. 사용 기록 전체
    usage_file = os.path.join(REPORT_DIR, f"사용기록_{now_str}.xlsx")
    df.to_excel(usage_file, index=False)

    print("[보고서 생성 완료]")
    print("→", invoice_file)
    print("→", stock_file)
    print("→", usage_file)