# character_graph
小説のキャラクターの関係図を構築するプログラム
```sh
- plot_chara_graph.py          # 関係図生成プログラム
- make_test_file.py            # 実験用のテキストファイル生成プログラム
- test.py                      # 簡単なテストがしたい時のプログラム実験場
  - test_1.py                  # 関係図系プログラムの実験場
```

# 使い方
1. make_test_file.pyで素の文章から形態素解析＋二つのラベル欄追加データへ移行
2. 手作業で人物情報ラベル（REL，NAME）と最長名ラベルを付与（ゆくゆくは自動化）
3. plot_chara_graph.pyで人物関係図を表示させたいデータを選んで表を描画
