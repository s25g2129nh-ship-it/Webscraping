import csv
import json
import requests


def get_gbo2_reviews():
    # バトオペ2のSteam AppID
    app_id = 1364780

    # Steam レビュー取得用 API
    url = f"https://store.steampowered.com/appreviews/{app_id}"
    params = {
        "json": 1,
        "language": "japanese",  # 日本語のレビュー
        "filter": "recent",  # recent（最新順）、updated（更新順）、all（おすすめ順）
        "num_per_page": 100,  # 1ページあたりの取得件数（最大100件）
        "purchase_type": "all",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("success") == 1:
            summary = data.get("query_summary", {})
            reviews = data.get("reviews", [])

            # 1. 総合評価・統計データの表示（コンソール）
            print("=== ゲームのストア評価サマリー ===")
            print(f"現在の評価ステータス : {summary.get('review_score_desc')}")
            print(f"総レビュー数 (条件内) : {summary.get('total_reviews')} 件")
            print(f"高評価数 (ポジティブ) : {summary.get('total_positive')} 件")
            print(f"低評価数 (ネガティブ) : {summary.get('total_negative')} 件")
            print("=======================================\n")

            # 2. CSVファイルへの書き込み処理
            csv_file_name = "gbo2_reviews.csv"

            # Excelでの文字化けを防ぐため 'utf_8_sig' を指定
            with open(
                csv_file_name, mode="w", encoding="utf_8_sig", newline=""
            ) as f:
                # CSVのヘッダー（列名）を定義
                fieldnames = ["番号", "判定", "総プレイ時間(時間)", "レビュー本文"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # ヘッダーを書き込む
                writer.writeheader()

                print(
                    f"--- 最新の日本語レビュー ({len(reviews)} 件) をCSVに出力中 ---"
                )
                for i, rev in enumerate(reviews, 1):
                    sentiment = (
                        "おすすめ" if rev.get("voted_up") else "おすすめしない"
                    )
                    playtime = (
                        rev.get("author", {}).get("playtime_forever", 0) // 60
                    )
                    review_text = rev.get("review", "").strip()

                    # CSVに1行ずつ書き込み
                    writer.writerow(
                        {
                            "番号": i,
                            "判定": sentiment,
                            "総プレイ時間(時間)": playtime,
                            "レビュー本文": review_text,
                        }
                    )

            print(f"\n保存が完了しました。ファイル名: {csv_file_name}")

        else:
            print("データの取得に失敗しました。")

    except requests.exceptions.RequestException as e:
        print(f"リクエストエラーが発生しました: {e}")


if __name__ == "__main__":
    get_gbo2_reviews()