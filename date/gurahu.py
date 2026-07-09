import matplotlib.pyplot as plt
import pandas as pd

# 1. データの読み込み
file_path = r"C:\Users\oojin\Documents\webスクレイピング\Webscraping\date\bad\Bad-analyzed\Shadowverse Worlds Beyond_ollama_analyzed.csv"
df = pd.read_csv(file_path)

# 2. データの集計
overall_counts = df["AI感情判定(Ollama)"].value_counts()

pos_df = df[df["AI感情判定(Ollama)"] == "positive"]
neg_df = df[df["AI感情判定(Ollama)"] == "negative"]
neu_df = df[df["AI感情判定(Ollama)"] == "neutral"]

pos_counts = pos_df["要因の分類"].value_counts()
neg_counts = neg_df["要因の分類"].value_counts()
neu_counts = neu_df["要因の分類"].value_counts()

# ★ フォントと全体のスタイル設定
plt.rcParams["font.family"] = "Yu Gothic"
plt.rcParams["font.size"] = 11
plt.rcParams["text.color"] = "#333333"

# 3. グラフの配置設定（2行 × 2列）
fig, axs = plt.subplots(2, 2, figsize=(14, 12))
((ax1, ax2), (ax3, ax4)) = axs

# 🎨 【重要】カラーパレットを「文字がハッキリ見える明るいパステル調」に変更
# 黒文字が綺麗に映える色を選んでいます
colors_main = ["#ff9999", "#99ff99", "#ffff99"]  # 明るい赤、明るい緑、明るい黄
colors_factors = [
    "#74b9ff",
    "#a29bfe",
    "#ffeaa7",
    "#81ecec",
    "#fab1a0",
]  # 明るい青、紫、黄、水色、オレンジ

# ★ ％の文字デザインを一括設定（太字、サイズ12、黒文字）
text_properties = {"fontsize": 12, "fontweight": "bold", "color": "#000000"}

# ── ① 左上：全体の比率 ──
wedges1, _, autotexts1 = ax1.pie(
    overall_counts,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
    colors=colors_main,
    pctdistance=0.75,
    textprops=text_properties,  # ★ ％の文字をクッキリさせる設定
)
ax1.legend(
    wedges1, overall_counts.index, title="感情判定", loc="center left", bbox_to_anchor=(1, 0.5)
)
ax1.set_title("1. 全体レビューの比率 (AI感情判定)", fontsize=13, fontweight="bold", pad=10)

# ── ② 右上：neutral の要因内訳 ──
if not neu_counts.empty:
    wedges2, _, autotexts2 = ax2.pie(
        neu_counts,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
        colors=colors_factors,
        pctdistance=0.75,
        textprops=text_properties,  # ★ ％の文字をクッキリさせる設定
    )
    ax2.legend(
        wedges2, neu_counts.index, title="要因の分類", loc="center left", bbox_to_anchor=(1, 0.5)
)
else:
    ax2.text(0.5, 0.5, "データなし", ha="center", va="center", fontsize=14, color="gray")
ax2.set_title("2. neutral の要因内訳", fontsize=13, fontweight="bold", pad=10)

# ── ③ 左下：positive の要因内訳 ──
wedges3, _, autotexts3 = ax3.pie(
    pos_counts,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
    colors=colors_factors,
    pctdistance=0.75,
    textprops=text_properties,  # ★ ％の文字をクッキリさせる設定
)
ax3.legend(
    wedges3, pos_counts.index, title="要因の分類", loc="center left", bbox_to_anchor=(1, 0.5)
)
ax3.set_title("3. positive の要因内訳", fontsize=13, fontweight="bold", pad=10)

# ── ④ 右下：negative の要因内訳 ──
wedges4, _, autotexts4 = ax4.pie(
    neg_counts,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
    colors=colors_factors,
    pctdistance=0.75,
    textprops=text_properties,  # ★ ％の文字をクッキリさせる設定
)
ax4.legend(
    wedges4, neg_counts.index, title="要因の分類", loc="center left", bbox_to_anchor=(1, 0.5)
)
ax4.set_title("4. negative の要因内訳", fontsize=13, fontweight="bold", pad=10)

# ★ 全体のメインタイトル設定
plt.suptitle("Shadowverse Worlds Beyond レビュー分析結果レポート", fontsize=18, fontweight="bold", y=0.96)

# ★ 配置の微調整
plt.tight_layout(rect=[0, 0, 0.9, 0.92])
plt.subplots_adjust(wspace=0.4, hspace=0.3)

# 4. 画像として保存
output_path = r"C:\Users\oojin\Documents\webスクレイピング\Webscraping\date\bad\Bad- graph\Shadowverse Worlds Beyond_graph.png"
plt.savefig(output_path, dpi=150, bbox_inches="tight")

print(f"視認性を改善したグラフを保存しました: {output_path}")

plt.show()