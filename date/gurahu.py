import matplotlib.pyplot as plt
import pandas as pd

# 1. データの読み込み
# 指定されたフォルダパスに修正しています
file_path = r"C:\Users\oojin\Documents\webスクレイピング\Webscraping\date\bad\Bad-analyzed\Call of Duty® Warzone™_ollama_analyzed.csv"
df = pd.read_csv(file_path)

# 2. データの集計
# 全体の比率用
overall_counts = df["判定"].value_counts()

# ポジティブとネガティブでフィルタリング
pos_df = df[df["判定"] == "おすすめ"]
neg_df = df[df["判定"] == "おすすめしない"]

pos_counts = pos_df["要因の分類"].value_counts()
neg_counts = neg_df["要因の分類"].value_counts()

# ★ フォント設定
plt.rcParams["font.family"] = "Yu Gothic"
plt.rcParams["font.size"] = 11

# 3. グラフの描画設定（3つの円グラフを並べるため横幅を広げる）
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 8))

# ── 左側：全体の比率 ──
ax1.pie(
    overall_counts,
    labels=overall_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
    colors=["#d62728", "#2ca02c"],  # おすすめしない=赤, おすすめ=緑
    pctdistance=0.7,
)
ax1.set_title("全体レビューの比率 (判定)", fontsize=14, fontweight="bold")

# ── 中央：ポジティブの円グラフ ──
ax2.pie(
    pos_counts,
    labels=pos_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
    pctdistance=0.75,
    labeldistance=1.1,
)
ax2.set_title("ポジティブ (おすすめ) の要因内訳", fontsize=14, fontweight="bold")

# ── 右側：ネガティブの円グラフ ──
ax3.pie(
    neg_counts,
    labels=neg_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
    pctdistance=0.75,
    labeldistance=1.1,
)
ax3.set_title("ネガティブ (おすすめしない) の要因内訳", fontsize=14, fontweight="bold")

# ★ メインタイトルの追加
plt.suptitle("Call of Duty® Warzone™ レビュー分析結果", fontsize=20, fontweight="bold")

# グラフが画面外にはみ出さないよう調整
plt.tight_layout(rect=[0, 0, 1, 0.95])

# ★ 画像として保存（指定のフォルダに保存されます）
output_path = r"C:\Users\oojin\Documents\webスクレイピング\Webscraping\date\bad\Bad- graph\COD_graph.png"
plt.savefig(output_path, dpi=150)

print(f"グラフを保存しました: {output_path}")

# 表示したい場合は plt.show() を追加してください
plt.show()