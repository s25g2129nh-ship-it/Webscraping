 Steamレビュー炎上分析


Steamゲームレビューデータを収集・分析し，高評価ゲームと炎上ゲームのレビューに見られる共通パターンを明らかにするプロジェクトです．

 概要

Steam Web APIを用いて複数ゲームの日本語レビューを収集し，以下の分析を行います．


ローカルAI（Ollama: gemma2:9b）による感情分析・要因分類
fugashiによる形態素解析 + ワードクラウド生成
matplotlibによる円グラフ可視化


千葉工業大学 認知情報科学実験１ の実験として実施しました．


ファイル構成

.
├── API.py                  # Steam APIでレビューを取得してCSVに保存
├── sentiment_analysis.py   # OllamaでCSVの感情分析・要因分類を実行
├── wordcloud_maker.py      # 形態素解析でワードクラウドを生成
├── gurahu.py               # 感情分析結果を円グラフで可視化
├── date/                   # 取得したレビューCSVの保存先
│   ├── big/                # 高評価ゲームのデータ
│   └── bad/                # 炎上ゲームのデータ
└── output/                 # ワードクラウド画像の出力先

 環境構築

必要なもの
Python 3.12
Ollama（ローカルAI実行環境）


ライブラリのインストール

bashpip install requests pandas wordcloud matplotlib fugashi unidic-lite tqdm

Ollamaのセットアップ

bash# Ollamaをインストール後，gemma2モデルを取得
ollama pull gemma2:9b


 使い方

① レビューの収集

API.py 内の app_id を取得したいゲームのSteam AppIDに変更して実行します．

bashpython API.py

実行するとレビューが gbo2_reviews.csv に保存されます．


Steam AppIDの調べ方
SteamストアページのURLに含まれる数字が AppID です．
例）https://store.steampowered.com/app/1364780/ → AppID は 1364780




② 感情分析・要因分類

sentiment_analysis.py 内の input_file_path を対象CSVのパスに変更して実行します．

bashpython sentiment_analysis.py

出力CSVには以下の列が追加されます．

列名内容AI感情判定(Ollama)positive / negative / neutral具体的な要因感情の引き金となったキーワード要因の分類ゲームシステム / 演出・グラフィック / ボリューム・価格 / 外部要因 / その他AIによる分析理由判定理由の1文説明


③ ワードクラウドの生成

wordcloud_maker.py 内のCSVパスを変更して実行します．

bashpython wordcloud_maker.py

output/ フォルダにタイムスタンプ付きのPNG画像が保存されます．


④ 円グラフの生成

gurahu.py 内のCSVパスと出力先パスを変更して実行します．

bashpython gurahu.py

以下の3種類の円グラフが1枚の画像として出力されます．


全体レビューのおすすめ/おすすめしない比率
ポジティブレビューの要因カテゴリ内訳
ネガティブレビューの要因カテゴリ内訳



 注意事項


Steam APIはAPIキー不要で利用できますが，1リクエストあたり最大100件までの取得制限があります．
本プロジェクトは日本語レビューのみを対象としています．
感情分析にはローカルAI（Ollama）を使用するため，外部へのデータ送信は発生しません．
wordcloud_maker.py のフォントパス（meiryo.ttc）はWindows環境を前提としています．macOS・Linuxの場合は適宜変更してください．



 各ファイルのパス変更箇所まとめ

ファイル変更箇所内容API.pyapp_id取得対象ゲームのSteam AppIDsentiment_analysis.pyinput_file_path分析対象のCSVパスsentiment_analysis.pyoutput_file_name出力CSVのファイル名wordcloud_maker.pydf = pd.read_csv(...)対象CSVのパスwordcloud_maker.pyfont_pathフォントファイルのパスgurahu.pyfile_path分析済みCSVのパスgurahu.pyoutput_pathグラフ画像の保存先パス


 メンバーと担当

平井　大尋：データ取得用のAPIを使用したプログラムの作成 
感情分析・要因分析用のプログラムを作成 
分析したデータを円グラフにするプログラムの作成 
円グラフの作成 

南　　翔太：主題の提案 
データ収集 
感情分析・要因分析 
WordCloud 作成プログラムの作成 
GitHubの活用 

今岡　奏　：データ収集 

片岡　悠斗：データ収集 
感情分析・要因分析 
WordCloud 作成プログラムの作成 
円グラフの作成 

中矢　翔太：データ収集 

　　　　　　TAとのミーティングの議事録作成 


 参考資料
 
Steam Web API ドキュメント
Ollama 公式サイト
fugashi ドキュメント
WordCloud ドキュメント
