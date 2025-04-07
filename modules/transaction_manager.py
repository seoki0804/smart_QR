import os
import pandas as pd
from datetime import datetime

TRANSACTION_FILE = "./database/transactions.xlsx"
os.makedirs("./database", exist_ok=True)

def append_transaction(item_id, item_name, intake=0, usage=0, request=0, memo=""):
    """
    거래 정보를 엑셀에 추가 저장

    Args:
        item_id (str): 고유 물품 ID
        item_name (str): 물품명
        intake (int): 수급량
        usage (int): 소모량
        request (int): 청구량
        memo (str): 비고
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_data = {
        "날짜": now,
        "item_id": item_id,
        "물품명": item_name,
        "수급량": intake,
        "소모량": usage,
        "청구량": request,
        "메모": memo
    }

    # 기존 파일이 있다면 이어서 추가
    if os.path.exists(TRANSACTION_FILE):
        df = pd.read_excel(TRANSACTION_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        df = pd.DataFrame([new_data])

    df.to_excel(TRANSACTION_FILE, index=False)
    print(f"[저장 완료] 거래 내역이 저장되었습니다 → {TRANSACTION_FILE}")