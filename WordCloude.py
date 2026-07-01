from importlib.resources import read_text
import os
from runpy import run_path
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from wordcloud import WordCloud

wordcloud = WordCloud(font_path=run_path, background_color="white").generate(read_text)

# ワードクラウドを表示
plt.figure(figsize=(8, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")  # 軸を非表示
plt.show()