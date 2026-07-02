import os
import json
import pandas as pd
import ollama
from tqdm import tqdm

# ==========================================
# ⚙️ 設定部分
# ==========================================
input_file_path = r"date/big/big-excel/WILDS.csv"
output_file_name = "WILDS_ollama_analyzed.csv"
# ==========================================

if not os.path.exists(input_file_path):
    print(f"エラー: ファイルが見つかりません: {input_file_path}")
    exit()

print("ファイルを読み込んでいます...")
try:
    df = pd.read_csv(input_file_path, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(input_file_path, encoding="cp932")

print(f"データを読み込みました。総件数: {len(df)}件")

prompt_template = """
以下のSteamのゲームレビュー（WILDS）を読み、文脈やスラング、ホラー表現を考慮して感情分析と要因分析を行ってください。

【分析ルール】
1. sentiment: 文章全体の本音から、[positive, negative, neutral] のいずれか1つを選んでください。
   ※ホラーゲームとして「怖い」「精神が壊れる」と褒めている場合は positive です。
   ※「おすすめ」に入っていても、ゲーム外の理由（映画化や組織の問題）で強い不満を述べている場合は negative です。
2. factor: ポジティブまたはネガティブな感情の引き金となった具体的な要素を「短いキーワード」で1つ抽出してください（例: ボリューム不足, 演出の見事さ, 映画化の配役, ルールのシンプルさ など）。
3. category: 要因が次のうちどれに該当するか、1つ選んでください：[ゲームシステム, 演出・グラフィック, ボリューム・価格, 外部要因・映画化, その他]
4. reason: なぜそのように判定したのか、レビューの文脈を踏まえて日本語で1文で説明してください。

【出力フォーマット】
必ず以下のJSON形式でのみ回答してください。余計な解説文やバッククォート(```)は一切不要です。文字列内に改行を含めないでください。
{{
  "sentiment": "positive",
  "factor": "要因キーワード",
  "category": "ゲームシステム",
  "reason": "～のため。"
}}

【分析対象のレビュー】
{review_text}
"""

sentiments = []
factors = []
categories = []
reasons = []

print("\nローカルAI（Ollama: gemma2）による感情・要因分析を実行中...")
print("※外部通信を行わないため、APIエラーは発生しません。")

for text in tqdm(df["レビュー本文"]):
    if not isinstance(text, str) or text.strip() == "":
        sentiments.append("neutral")
        factors.append("データなし")
        categories.append("その他")
        reasons.append("レビュー本文が空です。")
        continue
    
    clean_text = text.replace('"', "'").replace('\n', ' ').strip()
    formatted_prompt = prompt_template.format(review_text=clean_text)
    
    try:
        # パソコン内のOllamaを呼び出し
        response = ollama.chat(
            model='gemma2:9b',
            messages=[{'role': 'user', 'content': formatted_prompt}],
            options={'temperature': 0.1} # 出力を安定させる
        )
        
        raw_text = response['message']['content'].strip()
        
        # ```json などの余計なマークが付着した場合の除去
        if "```" in raw_text:
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        
        result = json.loads(raw_text.strip())
        
        sentiments.append(result.get("sentiment", "neutral"))
        factors.append(result.get("factor", "不明"))
        categories.append(result.get("category", "その他"))
        reasons.append(result.get("reason", "説明なし"))
        
    except Exception as e:
        sentiments.append("error")
        factors.append("解析失敗")
        categories.append("その他")
        reasons.append(f"AI出力の読み込みに失敗しました。")

# 結果の保存
df["AI感情判定(Ollama)"] = sentiments
df["具体的な要因"] = factors
df["要因の分類"] = categories
df["AIによる分析理由"] = reasons

df.to_csv(output_file_name, index=False, encoding="utf-8-sig")
print(f"\n✨ 分析が完了しました！結果を '{output_file_name}' に保存しました。")