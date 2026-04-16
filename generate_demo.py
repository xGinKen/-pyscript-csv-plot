"""デモ用 CSV を生成するスクリプト。
10000 行 × 3 列 (秒, 合計件数, 問い合わせ件数) を 24 時間 (86400 秒) に分散。
業務時間帯 (9-18時) にピークを持つ現実的な日次パターンを再現する。
"""
import csv
import math
import random
from pathlib import Path

random.seed(42)

N_ROWS = 10000
DAY_SEC = 24 * 3600  # 86400

out = Path(__file__).with_name("demo.csv")

with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["秒", "合計件数", "問い合わせ件数"])

    for i in range(N_ROWS):
        # 0 .. 86400 を 10000 点で等分
        sec = round(i * DAY_SEC / (N_ROWS - 1))
        hour = sec / 3600.0

        # 業務時間帯 (13時頃ピーク) を中心にしたガウス型の日次パターン
        peak = math.exp(-((hour - 13.0) ** 2) / (2 * 3.0 ** 2))  # σ=3h
        base = 5 + 95 * peak  # 5 〜 ~100

        total = max(0, int(base + random.gauss(0, 6)))
        # 問い合わせ件数は合計の 20〜40% 程度
        ratio = 0.30 + 0.10 * math.sin(hour / 24.0 * 2 * math.pi)
        inquiry = max(0, int(total * ratio + random.gauss(0, 2)))
        inquiry = min(inquiry, total)  # 合計を超えないように

        w.writerow([sec, total, inquiry])

print(f"Wrote {N_ROWS} rows to {out}")
