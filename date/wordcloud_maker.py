import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from fugashi import Tagger
import re

# ===== 1. CSV の読み込み =====
# ★ CSV のパスを自分の環境に合わせて変更
df = pd.read_csv(r"C:\Users\Mizuk\Documents\APEX.csv", encoding="utf-8")

# レビュー本文をすべて結合
text_data = " ".join(df["レビュー本文"].dropna().astype(str).tolist())

# ===== 2. 日本語形態素解析（名詞だけ抽出） =====
tagger = Tagger()
tokens = []

for word in tagger(text_data):
    # Unidic の品詞は pos1 に入っている
    if word.feature.pos1 == "名詞":
        tokens.append(word.surface)

# ===== 3. ノイズ除去 =====
cleaned_words = []

for w in tokens:
    # 英数字1文字
    if re.fullmatch(r"[a-zA-Z0-9]", w):
        continue

    # 記号
    if re.fullmatch(r"[!-/:-@[-`{-~]", w):
        continue

    # ひらがな2〜3文字
    if re.fullmatch(r"[ぁ-ん]{2,3}", w):
        continue

    # ひらがなのみ（長さ問わず）
    if re.fullmatch(r"[ぁ-ん]+", w):
        continue

    # 1文字の単語を除外
    if len(w) <= 1:
        continue

    cleaned_words.append(w)

# ===== 4. ストップワード =====
stopwords = {
    "する", "いる", "ある", "こと", "よう", "ため",
    "これ", "それ", "あれ", "さん", "ます", "です",
    "感じ", "部分", "自分", "今回", "場合", "ところ",
    "時", "人", "方", "的", "中"
}

cleaned_words = [w for w in cleaned_words if w not in stopwords]

# ===== 5. フォント設定（あなたの環境で読み込めるフォント） =====
font_path = r"C:\Windows\Fonts\meiryo.ttc"

print("使用フォント:", font_path)  # ← 確認用

# ===== 6. ワードクラウド生成 =====
wordcloud = WordCloud(
    width=1200,
    height=800,
    background_color="white",
    font_path=font_path,
    collocations=False,
    max_font_size=150
).generate(" ".join(cleaned_words))

# ===== 7. 表示 =====
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.show()
