import sys
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QMessageBox

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDoリストアプリ")  # ウィンドウのタイトル設定
        self.setGeometry(100, 100, 400, 400)  # ウィンドウサイズと位置
        
        self.layout = QVBoxLayout()
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("タスクを入力")  
        
        self.add_button = QPushButton("追加", self)
        self.add_button.clicked.connect(self.add_task)  # 追加ボタンのクリックイベント
        
        self.task_list = QListWidget(self) 
        
        self.delete_button = QPushButton("削除", self)
        self.delete_button.clicked.connect(self.delete_task)  # 削除ボタンのクリックイベント
        
        # レイアウトにウィジェットを追加
        self.layout.addWidget(self.task_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.task_list)
        self.layout.addWidget(self.delete_button)
        
        self.setLayout(self.layout)  
        self.load_tasks()  

    def add_task(self):
        task = self.task_input.text().strip()  # 入力テキストを取得し、空白を削除
        if task:
            self.task_list.addItem(task)  # リストにタスクを追加
            self.task_input.clear()  # 入力欄をクリア
            self.save_tasks()  # タスクを保存
        else:
            QMessageBox.warning(self, "警告", "タスクを入力してください！")  # 入力が空なら警告を表示
    
    def delete_task(self):
        selected_task = self.task_list.currentRow()  
        if selected_task >= 0:
            self.task_list.takeItem(selected_task)  # 選択されたタスクを削除
            self.save_tasks()  # 削除後にタスクを保存
        else:
            QMessageBox.warning(self, "警告", "削除するタスクを選択してください！")  # 選択なしなら警告
    
    def save_tasks(self):
        tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]  # 現在のタスクをリストに格納
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)  # JSONファイルに保存
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                tasks = json.load(file)
                self.task_list.addItems(tasks)  # 読み込んだタスクをリストに追加
        except FileNotFoundError:
            pass  # ファイルが存在しない場合は何もしない

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()  # ウィンドウを表示
    sys.exit(app.exec())  # アプリを実行
