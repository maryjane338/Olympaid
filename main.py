from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import pandas as pd
import csv


class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.file = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Результаты олимпиады: фильтрация")
        self.resize(700, 500)

        self.school_box = QComboBox()
        self.school_box.addItem('Все')
        self.grade_box = QComboBox()
        self.grade_box.addItem('Все')

        self.results = QPushButton('Узнать результаты')
        self.results.clicked.connect(self.filtration)
        self.open_btn = QPushButton('Открыть файл')
        self.open_btn.clicked.connect(self.open)

        self.view = QTableView()

        v_l1 = QVBoxLayout()
        h_l1 = QHBoxLayout()
        v_l1.addLayout(h_l1)
        h_l1.addWidget(self.school_box)
        h_l1.addWidget(self.grade_box)
        h_l1.addWidget(self.results)
        h_l1.addWidget(self.open_btn)
        v_l1.addWidget(self.view)
        self.setLayout(v_l1)

    def open(self):
        self.file = QFileDialog.getOpenFileName(self, 'Выберите файл')[0]
        if self.file:
            with open(self.file, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                self.rows = list(reader)

                self.filtration()

                not_duplicate_school = []
                for i in self.school:
                    if i not in not_duplicate_school:
                        not_duplicate_school.append(i)
                not_duplicate_grade = []
                for i in self.grade:
                    if i not in not_duplicate_grade:
                        not_duplicate_grade.append(i)
                self.school_box.addItems(sorted(not_duplicate_school))
                self.grade_box.addItems(sorted(not_duplicate_grade))
        else:
            message = QMessageBox()
            message.setWindowTitle('Инфо')
            message.setText('Файл не выбран')
            message.exec()

    def filtration(self):
        self.surnames = []
        self.scores = []
        self.user = []
        self.school = []
        self.grade = []
        for row in self.rows:
            a = row[1]
            b = row[2]
            list1 = a.split(' ')
            list2 = b.split('-')
            self.surnames.append(list1[3])
            self.scores.append(row[7])
            self.user.append(row[1])
            self.school.append(list2[2])
            self.grade.append(list2[3])
        results = {'surname': self.surnames,
                   'scores': self.scores,
                   'user_name': self.user,
                   'school': self.school,
                   'grade': self.grade}
        self.results_df = pd.DataFrame(results)

        if self.file is not None:
            if self.school_box.currentText() != 'Все':
                fltr = self.results_df.school == self.school_box.currentText()
                df = self.results_df.loc[fltr, :]
            else:
                df = self.results_df
            if self.grade_box.currentText() != 'Все':
                fltr2 = df.grade == self.grade_box.currentText()
                df = df.loc[fltr2, :]
            else:
                df = df

            scores = list(map(int, df.scores))
            win_scores_int = sorted(set(scores), reverse=True)[:3]
            win_scores_int = ' '.join([str(elem) for elem in win_scores_int])
            win_scores = win_scores_int.split(' ')
            if len(win_scores) == 3:
                gold_fltr = df.scores == win_scores[0]
                silver_fltr = df.scores == win_scores[1]
                bronze_fltr = df.scores == win_scores[2]
                gold_df = df.loc[gold_fltr, :]
                silver_df = df.loc[silver_fltr, :]
                bronze_df = df.loc[bronze_fltr, :]
                number_gold_df = gold_df.shape[0]
                number_silver_df = silver_df.shape[0]
                number_bronze_df = bronze_df.shape[0]
            elif len(win_scores) == 2:
                gold_fltr = df.scores == win_scores[0]
                silver_fltr = df.scores == win_scores[1]
                gold_df = df.loc[gold_fltr, :]
                silver_df = df.loc[silver_fltr, :]
                number_gold_df = gold_df.shape[0]
                number_silver_df = silver_df.shape[0]
            elif len(win_scores) == 1:
                gold_fltr = df.scores == win_scores[0]
                gold_df = df.loc[gold_fltr, :]
                number_gold_df = gold_df.shape[0]

            gold_color = QColor(255, 215, 0)
            silver_color = QColor(192, 192, 192)
            bronze_color = QColor(205, 127, 50)

            del df['scores']
            df.insert(1, 'scores', scores)
            df = df.sort_values(by='scores', ascending=False)
            scores2_list = list(df.scores)
            scores_int = ' '.join([str(elem) for elem in scores2_list])
            scores_str = scores_int.split(' ')
            del df['scores']
            df.insert(1, 'scores', scores_str)
            scores_item = list(df.scores)
            user_item = list(df.user_name)
            surnames_item = list(df.surname)
            print(df)
            model2 = QStandardItemModel()
            model2.setHorizontalHeaderLabels(["Фамилия", "Результат", "Логин"])
            for i, (score, user_login, surname) in enumerate(zip(scores_item, user_item, surnames_item)):
                item1 = QStandardItem(surname)
                item2 = QStandardItem(score)
                item3 = QStandardItem(user_login)

                if i < number_gold_df:
                    item1.setBackground(gold_color)
                    item2.setBackground(gold_color)
                    item3.setBackground(gold_color)
                elif i < number_gold_df + number_silver_df:
                    item1.setBackground(silver_color)
                    item2.setBackground(silver_color)
                    item3.setBackground(silver_color)
                elif i < number_gold_df + number_silver_df + number_bronze_df:
                    item1.setBackground(bronze_color)
                    item2.setBackground(bronze_color)
                    item3.setBackground(bronze_color)

                model2.appendRow([item1, item2, item3])
            self.view.setModel(model2)
        else:
            message = QMessageBox()
            message.setWindowTitle('Инфо')
            message.setText('Вы не открыли файл.')
            message.exec()

def main():
    app = QApplication([])
    win = MainWin()
    win.show()
    app.exec()


if __name__ == '__main__':
    main()
