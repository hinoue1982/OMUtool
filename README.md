# \# JUSTDWH検査データ整理 説明書

対象バージョン: 0.2

# \# About

REDCapから出してきたRecord_idおよび患者IDを含むワイドタイプのcsvファイル(症例データcsv)に、JUSTDWHから出してきたロングタイプのcsvファイル（検査データcsv)を、症例データの各レコードごとに基準日から指定した範囲のデータを検索・抽出し、連結するソフトウェアです。

# \# 使い方

Python3が使える方はpythonファイルを使用していただいて結構です。ライブラリとしてpandasが必要になります。


自身のPCでpython3が使用できない場合は Releasesから .exeファイルをダウンロードして使用してください。この場合、他に必要なファイル、アプリなどはありません。。
