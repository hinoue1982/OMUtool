import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk
import pandas as pd


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.version = "0.2"

        master.title(f"JUSTDWH検査データ整理 Version {self.version}")
        master.geometry("800x420")
        self.grid(row=0, column=0, sticky=tk.W)

        # 変数
        self.id_case = tk.StringVar()
        self.base_date_case = tk.StringVar()
        self.data_window_start = tk.IntVar()
        self.data_window_end = tk.IntVar()
        self.id_labo = tk.StringVar()
        self.base_date_labo = tk.StringVar()
        self.labo_name = tk.StringVar()
        self.labo_result = tk.StringVar()
        self.collected_name = tk.StringVar()
        self.collected_data_process = tk.StringVar()
        self.collected_data_process_dict = {
            "最も古い日付のデータ": 0,
            "最新のデータ": -1,
        }
        self.export_column_name = tk.StringVar()
        self.export_file_name = tk.StringVar()
        self.collected_data = pd.DataFrame()
        self.collected_data_name_list = list()

        # ウィジェット作成
        self.create_widgets_case()
        self.create_widgets_labo()
        self.create_widgets_collection()

    def create_widgets_case(self):
        # 症例csv関連のフレーム
        self.frm_case = ttk.Frame(self, padding=10)
        self.frm_case.grid(row=0, column=0, sticky=tk.W)

        # 症例csvファイル読み込み
        self.btn_read_csv_case = ttk.Button(
            self.frm_case,
            text="症例csv読み込み (こちらのIDを基準にデータを連結)",
            command=self.read_csv_case,
        )
        self.btn_read_csv_case.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.label_csv_case = ttk.Label(self.frm_case, text="未選択")
        self.label_csv_case.grid(row=0, column=2, columnspan=2)

        # 症例csvのID列
        self.title_id_case = ttk.Label(self.frm_case, text="ID列")
        self.title_id_case.grid(row=1, column=0)
        self.cbx_id_case = ttk.Combobox(
            self.frm_case, values=None, state="readonly", textvariable=self.id_case
        )
        self.cbx_id_case.grid(row=1, column=1, sticky=tk.W)
        self.cbx_id_case.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_head_data(
                self.df_case, self.cbx_id_case, self.head_id_case
            ),
        )
        self.head_id_case = ttk.Label(self.frm_case, text=None)
        self.head_id_case.grid(row=1, column=2, sticky=tk.W)

        # 症例csvの基準日列
        self.title_base_date_case = ttk.Label(self.frm_case, text="データ収集基準日列")
        self.title_base_date_case.grid(row=2, column=0)

        self.cbx_base_date_case = ttk.Combobox(
            self.frm_case,
            values=None,
            state="readonly",
            textvariable=self.base_date_case,
        )
        self.cbx_base_date_case.grid(row=2, column=1, sticky=tk.W)
        self.cbx_base_date_case.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_head_data(
                self.df_case, self.cbx_base_date_case, self.head_base_date_case
            ),
        )

        self.head_base_date_case = ttk.Label(self.frm_case, text=None)
        self.head_base_date_case.grid(row=2, column=2, sticky=tk.W)

    def create_widgets_labo(self):
        # ラボデータ側csv関連のウィジェット用フレーム
        self.frm_labo = ttk.Frame(self, padding=10)
        self.frm_labo.grid(row=1, column=0, sticky=tk.W)

        # ラボデータcsvファイル読み込み
        self.btn_read_csv_labo = ttk.Button(
            self.frm_labo, text="検査データcsv読み込み", command=self.read_csv_labo
        )
        self.btn_read_csv_labo.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.label_csv_labo = ttk.Label(self.frm_labo, text="未選択")
        self.label_csv_labo.grid(row=0, column=2, columnspan=2, sticky=tk.W)

        # ラボデータのID列
        self.title_id_labo = ttk.Label(self.frm_labo, text="ID列")
        self.title_id_labo.grid(row=1, column=0, sticky=tk.W)

        self.cbx_id_labo = ttk.Combobox(
            self.frm_labo, values=None, state="readonly", textvariable=self.id_labo
        )
        self.cbx_id_labo.grid(row=1, column=1, sticky=tk.W)
        self.cbx_id_labo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_head_data(
                self.df_labo, self.cbx_id_labo, self.head_id_labo
            ),
        )
        self.head_id_labo = ttk.Label(self.frm_labo, text=None)
        self.head_id_labo.grid(row=1, column=2, sticky=tk.W)

        # ラボデータの検査日列
        self.title_base_date_labo = ttk.Label(
            self.frm_labo, text="検査データの検査日列"
        )
        self.title_base_date_labo.grid(row=2, column=0)

        self.cbx_base_date_labo = ttk.Combobox(
            self.frm_labo,
            values=None,
            state="readonly",
            textvariable=self.base_date_labo,
        )
        self.cbx_base_date_labo.grid(row=2, column=1, sticky=tk.W)
        self.cbx_base_date_labo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_head_data(
                self.df_labo, self.cbx_base_date_labo, self.head_base_date_labo
            ),
        )
        self.head_base_date_labo = ttk.Label(self.frm_labo, text=None)
        self.head_base_date_labo.grid(row=2, column=2, sticky=tk.W)

        # ラボデータの検査項目名列
        self.title_labo_name = ttk.Label(self.frm_labo, text="検査データの項目名列")
        self.title_labo_name.grid(row=3, column=0)

        self.cbx_labo_name = ttk.Combobox(
            self.frm_labo, values=None, state="readonly", textvariable=self.labo_name
        )
        self.cbx_labo_name.grid(row=3, column=1, sticky=tk.W)
        self.cbx_labo_name.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_head_data(
                self.df_labo, self.cbx_labo_name, self.head_labo_name
            ),
        )
        self.cbx_labo_name.bind(
            "<<ComboboxSelected>>", lambda event: self.update_test_list(), "+"
        )
        self.head_labo_name = ttk.Label(self.frm_labo, text=None)
        self.head_labo_name.grid(row=3, column=2)

        # ラボデータの結果列
        self.title_labo_result = ttk.Label(self.frm_labo, text="検査データの結果列")
        self.title_labo_result.grid(row=4, column=0, sticky=tk.W)

        self.cbx_labo_result = ttk.Combobox(
            self.frm_labo, values=None, state="readonly", textvariable=self.labo_result
        )
        self.cbx_labo_result.grid(row=4, column=1, sticky=tk.W)
        self.cbx_labo_result.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_head_data(
                self.df_labo, self.cbx_labo_result, self.head_labo_result
            ),
        )
        self.head_labo_result = ttk.Label(self.frm_labo, text=None)
        self.head_labo_result.grid(row=4, column=2, sticky=tk.W)

        # 選択する検査
        self.title_selected_test = ttk.Label(self.frm_labo, text="収集する検査名")
        self.title_selected_test.grid(row=5, column=0, sticky=tk.W)

        self.cbx_selected_test = ttk.Combobox(
            self.frm_labo,
            values=None,
            state="readonly",
            textvariable=self.collected_name,
        )
        self.cbx_selected_test.bind(
            "<<ComboboxSelected>>",
            lambda event: self.export_column_name.set(self.collected_name.get()),
        )
        self.cbx_selected_test.grid(row=5, column=1, sticky=tk.W)

        # 症例csvからデータ抽出する際の抽出期間
        self.title_data_window_start = ttk.Label(
            self.frm_labo, text="データ収集期間(日)"
        )
        self.title_data_window_start.grid(row=6, column=0, sticky=tk.W)

        self.frm_data_window = ttk.Frame(self.frm_labo)
        self.frm_data_window.grid(row=6, column=1, columnspan=2, sticky=tk.W)

        # 開始日
        self.entry_data_window_start = ttk.Entry(
            self.frm_data_window, textvariable=self.data_window_start
        )
        self.entry_data_window_start.grid(row=0, column=0)

        self.label_data_window_inter = ttk.Label(self.frm_data_window, text="～")
        self.label_data_window_inter.grid(row=0, column=1)

        # 終了日
        self.entry_data_window_end = ttk.Entry(
            self.frm_data_window, textvariable=self.data_window_end
        )
        self.entry_data_window_end.grid(row=0, column=2, sticky=tk.W)

    def create_widgets_collection(self):
        # データ収集関連のウィジェット
        self.frm_collection = ttk.Frame(self, padding=10)
        self.frm_collection.grid(row=2, column=0, sticky=tk.W)

        # 保存時の収集データ列名
        self.title_export_column_name = ttk.Label(
            self.frm_collection, text="保存時の収集データ列名"
        )
        self.title_export_column_name.grid(row=0, column=0, sticky=tk.W)
        self.entry_export_column_name = ttk.Entry(
            self.frm_collection, textvariable=self.export_column_name
        )
        self.entry_export_column_name.grid(row=0, column=1, sticky=tk.W)

        # 複数回検査の場合の収集タイミング
        self.title_collected_data_process = ttk.Label(
            self.frm_collection, text="複数回検査の処理"
        )
        self.title_collected_data_process.grid(row=1, column=0, sticky=tk.W)
        self.cbx_collected_data_process = ttk.Combobox(
            self.frm_collection,
            values=list(self.collected_data_process_dict.keys()),
            textvariable=self.collected_data_process,
        )
        self.cbx_collected_data_process.grid(row=1, column=1, sticky=tk.W)

        # データ収集ボタン
        self.btn_collect_data = ttk.Button(
            self.frm_collection, text="データ収集", command=self.collect_data
        )
        self.btn_collect_data.grid(row=2, column=0, sticky=tk.W)

        # 収集したデータの表示
        self.label_collect_data = ttk.Label(self.frm_collection, text=None)
        self.label_collect_data.grid(row=2, column=1, sticky=tk.W)

        # データ保存ボタン
        self.btn_export_data = ttk.Button(
            self.frm_collection, text="データ保存", command=self.export_data
        )
        self.btn_export_data.grid(row=3, column=0, sticky=tk.W)

    def read_csv_case(self):
        # 症例データcsvのパスを得る
        self.path_csv_case = fd.askopenfilename(filetypes=[("", "*.csv")])
        self.label_csv_case.configure(text=self.path_csv_case)

        # データフレームとして読み込み
        self.df_case = pd.read_csv(self.path_csv_case, encoding="cp932")
        self.df_case_columns = list(self.df_case.columns)

        # collected_dataにIDいれる
        self.collected_data["record_id"] = self.df_case["record_id"]

        # ID、基準日列のコンボボックスの列名リスト設定
        self.cbx_id_case["values"] = self.df_case_columns
        self.cbx_base_date_case["values"] = self.df_case_columns

    def read_csv_labo(self):
        # ラボデータcsvのパスを得る
        self.path_csv_labo = fd.askopenfilename(filetypes=[("", "*.csv")])
        self.label_csv_labo.configure(text=self.path_csv_labo)

        # データフレームとして読み込み
        self.df_labo = pd.read_csv(self.path_csv_labo, encoding="cp932")
        self.df_labo_columns = list(self.df_labo.columns)

        # ID、検査日、検査名、結果のコンボボックスに列名リスト設定
        self.cbx_id_labo["values"] = self.df_labo_columns
        self.cbx_base_date_labo["values"] = self.df_labo_columns
        self.cbx_labo_name["values"] = self.df_labo_columns
        self.cbx_labo_result["values"] = self.df_labo_columns

        # 検査項目名列が設定されている場合、そのリストを取得
        if self.labo_name.get() in self.df_labo_columns:
            unique_tests = self.df_labo[self.labo_name.get()].dropna().unique()
            self.cbx_selected_test["values"] = sorted(unique_tests)
        else:
            self.cbx_selected_test["values"] = []

    def show_head_data(self, dataframe, combobox, label):
        # 列を選んだ際に先頭5行を例として表示
        label.configure(
            text=f'例: {", ".join(dataframe[combobox.get()][0:5].astype("str"))}'
        )

    def preprocess_df_case(self):
        # 日付の形式をdatetimeに
        self.df_case[self.base_date_case.get()] = pd.to_datetime(
            self.df_case[self.base_date_case.get()], format="%Y/%m/%d"
        )

    def preprocess_df_labo(self):
        # 採血から重複データ削除
        self.df_labo = self.df_labo.drop_duplicates().reset_index(drop=True)
        # 日付の形式をdatetimeに
        self.df_labo[self.base_date_labo.get()] = pd.to_datetime(
            self.df_labo[self.base_date_labo.get()], format="%Y%m%d"
        )

    def update_test_list(self):
        # 検査項目名列からユニークな検査名リストを取得して更新
        selected_labo_name_col = self.labo_name.get()
        if selected_labo_name_col in self.df_labo_columns:
            unique_tests = self.df_labo[selected_labo_name_col].dropna().unique()
            self.cbx_selected_test["values"] = sorted(unique_tests)
        else:
            self.cbx_selected_test["values"] = []

    def collect_data(self):
        self.preprocess_df_case()
        self.preprocess_df_labo()

        # 入力データを取得
        id_case_col = self.id_case.get()
        base_date_case_col = self.base_date_case.get()
        data_window_start = self.data_window_start.get()
        data_window_end = self.data_window_end.get()
        id_labo_col = self.id_labo.get()
        base_date_labo_col = self.base_date_labo.get()
        selected_test = self.collected_name.get()
        new_column_name = self.export_column_name.get()
        data_process_option = self.collected_data_process.get()

        # 症例データの範囲抽出
        self.df_case["start_date"] = self.df_case[base_date_case_col] + pd.to_timedelta(
            data_window_start, unit="d"
        )
        self.df_case["end_date"] = self.df_case[base_date_case_col] + pd.to_timedelta(
            data_window_end, unit="d"
        )

        # ラボデータの検査項目フィルタリング
        filtered_labo = self.df_labo[
            self.df_labo[self.labo_name.get()] == selected_test
        ]

        # 症例データとフィルタリング済みラボデータの結合
        merged_data = pd.merge(
            self.df_case,
            filtered_labo,
            left_on=id_case_col,
            right_on=id_labo_col,
            how="left",
        )

        filtered_data = merged_data[
            (
                (merged_data[base_date_labo_col] >= merged_data["start_date"])
                & (merged_data[base_date_labo_col] <= merged_data["end_date"])
            )
        ]

        # 複数回検査の処理
        # TODO: 他の処理法を必要に応じて実装
        # TODO: 項目が増えた場合に if分岐でない方法に変更
        if data_process_option == "最も古い日付のデータ":
            filtered_data = filtered_data.loc[
                filtered_data.groupby("record_id")[base_date_labo_col].idxmin()
            ]
        elif data_process_option == "最新のデータ":
            filtered_data = filtered_data.loc[
                filtered_data.groupby("record_id")[base_date_labo_col].idxmax()
            ]

        # 必要な列を選択
        selected_columns = [
            "record_id",
            self.labo_result.get(),
        ]

        result_data = filtered_data[
            [col for col in selected_columns if col in merged_data.columns]
        ].copy()

        # 列名の変更, collected_data_name_listに付け加え
        if new_column_name:  # 入力がある場合、列名を変更
            result_data.rename(
                columns={self.labo_result.get(): new_column_name}, inplace=True
            )
            self.collected_data_name_list.append(new_column_name)
        else:
            self.collected_data_name_list.append(self.collected_name)

        self.collected_data = pd.merge(
            self.collected_data, result_data, on="record_id", how="left"
        )
        self.label_collect_data.configure(
            text=f"収集済: {self.collected_data_name_list}"
        )

        # 最後にdf_caseから余分な列を落とす
        self.df_case = self.df_case.drop(["start_date", "end_date"], axis=1)

    def export_data(self):
        # df_caseとcollected_dataを結合
        export_data = pd.merge(
            self.df_case, self.collected_data, on="record_id", how="left"
        )

        # 保存先を選択
        save_path = fd.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if save_path:
            export_data.to_csv(save_path, index=False, encoding="cp932")
            tk.messagebox.showinfo("完了", f"データが保存されました: {save_path}")
        else:
            tk.messagebox.showwarning("警告", "保存がキャンセルされました。")


# classの後に記入する
root = tk.Tk()
app = App(master=root)
app.mainloop()

# TODO: 設定ファイルを読み込んで一括処理できるようにする。
