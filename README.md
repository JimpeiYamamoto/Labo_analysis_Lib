# Labo_analysis_Lib
研究で使用するデータを解析する用に自作したライブラリ
## 対応機器
- ALS 電気化学アナライザー
- 日立ハイテクサイエンス 蛍光分光光度計
## 使用方法
### インストール
```
git clone git@github.com:JimpeiYamamoto/Labo_analysis_Lib.git
```
### インポート
```py
#ALSの電気化学アナライザー用の関数を使用する場合
from Labo_analysis_Lib import LibCV
#日立ハイテクサイエンス蛍光分光光度計用の関数を使用する場合
from Labo_analysis_Lib import LibEEM
```
## 関数
### LibCV
- `def show_cv_graph(df_name_lst)`
- `def cv_file_to_df(df_name)`
### LibEEM
- `def eem_file_to_df(file_path)`
- `def show_eem_graph(df, span_set=False, max_=10, min_=-10)`
- `def show_calibration_curve(df, ex, em, dic)`
- `def time_eem_file_to_df(path)`
- `def time_plt(df)`
- `def all_csv_to_many_txt(eem_path, save_path)`
- `def calcu_std(df, ex, em)`
- `def show_time_intensity(df, ex, em, max_, min_)`

## お問い合わせ
- 質問や要望があれば twitter: `@yjimpei_10` まで