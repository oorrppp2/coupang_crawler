import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QScrollArea, QVBoxLayout, QHBoxLayout, QMessageBox)
from coupang_crawler import coupang_crawler

class Coupang_UI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.coupang_crawler = coupang_crawler()

    def initUI(self):
        self.window_layout = QVBoxLayout(self)

        self.instance_layout = QHBoxLayout(self)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.instance_grid = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.instance_layout.addWidget(self.scrollArea)

        self.url_layout = QGridLayout(self)

        self.window_layout.addLayout(self.instance_layout)
        self.window_layout.addLayout(self.url_layout)
        self.setLayout(self.window_layout)

        self.instance_list = []
        self.add_btn = QPushButton("추가", self)
        self.refresh_btn = QPushButton("총액갱신", self)
        self.exit_btn = QPushButton("프로그램 종료", self)
        self.save_btn = QPushButton("엑셀로 내보내기", self)
        self.total = 0
        self.total_label = QLabel("총액: {0}₩".format(self.total))
        self.add_btn.clicked.connect(self.push_add_button)
        self.refresh_btn.clicked.connect(self.push_refresh_button)
        self.exit_btn.clicked.connect(self.push_exit_button)
        self.save_btn.clicked.connect(self.push_save_button)

        self.url_editline = QLineEdit()
        self.quantity_editline = QLineEdit()

        self.url_layout.addWidget(QLabel('쿠팡 상품 url 주소:'), 0, 0)
        self.url_layout.addWidget(QLabel('수량:'), 1, 0)

        self.url_layout.addWidget(self.url_editline, 0, 1)
        self.url_layout.addWidget(self.quantity_editline, 1, 1)

        self.url_layout.addWidget(self.add_btn, 2, 0)
        self.url_layout.addWidget(self.refresh_btn, 2, 1)
        self.url_layout.addWidget(self.total_label, 2, 2)

        self.url_layout.addWidget(self.save_btn, 3, 1)
        self.url_layout.addWidget(self.exit_btn, 3, 2)

        name_label = QLabel('제품명')
        quant_label = QLabel('수량')
        unit_price_label = QLabel('단가')
        total_price_label = QLabel('총 가격')
        self.instance_grid.addWidget(name_label, 0, 0)
        self.instance_grid.addWidget(quant_label, 0, 1)
        self.instance_grid.addWidget(unit_price_label, 0, 2)
        self.instance_grid.addWidget(total_price_label, 0, 3)

        self.setWindowTitle('쿠팡 간식 주문 마법사')
        self.setGeometry(300, 300, 500, 100)
        self.show()

    def push_add_button(self):
        # 크롤러 클래스를 이용해 정보 가져오기
        try:
            url = self.url_editline.text()
            quantity = int(self.quantity_editline.text())
            if quantity < 0:
                QMessageBox.warning(self, "Error", "올바른 값을 입력해주세요.")
                return
            product_name, quantity, price = self.coupang_crawler.get_instance(url, quantity)
        except:
            QMessageBox.warning(self, "Error", "올바른 값을 입력해주세요.")
            return
        
        new_name_instance = QLineEdit(product_name)
        new_quant_instance = QLineEdit(str(quantity))
        new_unit_price_instance = QLineEdit(str(int(price)))
        new_total_price_instance = QLineEdit(str(int(price) * quantity))
        new_instance = {"name":new_name_instance, "quantity":new_quant_instance, "unit_price":new_unit_price_instance, "total_price": new_total_price_instance, "link":url}
        self.instance_list.append(new_instance)

        self.instance_grid.addWidget(new_name_instance, len(self.instance_list), 0)
        self.instance_grid.addWidget(new_quant_instance, len(self.instance_list), 1)
        self.instance_grid.addWidget(new_unit_price_instance, len(self.instance_list), 2)
        self.instance_grid.addWidget(new_total_price_instance, len(self.instance_list), 3)

        new_unit_price_instance.setEnabled(False)
        new_total_price_instance.setEnabled(False)

        self.url_editline.clear()
        self.quantity_editline.clear()
        self.push_refresh_button()

    def push_refresh_button(self):
        total = 0
        try:
            for i, instance in enumerate(self.instance_list):
                if int(instance["quantity"].text()) < 0:
                    QMessageBox.warning(self, "Error", "수량 중 음수가 있습니다.\n수량을 확인하고 다시 시도하세요.")
                    return
                new_total_price = int(instance["unit_price"].text()) * int(instance["quantity"].text())
                total += new_total_price
                instance["total_price"].setText(str(new_total_price))
        except:
            QMessageBox.warning(self, "Error", "수량에 문자가 포함 되어 있습니다..")
        

        self.total_label.setText("총액: {0:,d}₩".format(total))
        if total > 500000:
            self.total_label.setStyleSheet("color: red;")
        else:
            self.total_label.setStyleSheet("color: black;")
        self.total = total

    def push_save_button(self):
        instances_dict_list = []
        for instance in self.instance_list:
            if int(instance["quantity"].text()) == 0:
                continue
            instance_dict = {}
            instance_dict["product_name"] = instance["name"].text()
            instance_dict["quantity"] = instance["quantity"].text()
            instance_dict["price"] = int(instance["price"].text())
            instance_dict["link"] = instance["link"]
            instances_dict_list.append(instance_dict)
        self.coupang_crawler.save_pyxl(instances_dict_list, self.total)
        if os.path.isfile('./data/coupang.xlsx'):
            QMessageBox.information(self, "Success", "엑셀로 내보내기 성공!")
        else:
            QMessageBox.warning(self, "Error", "엑셀로 내보내는데 실패했습니다.")


    def push_exit_button(self):
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coupang_UI()
    sys.exit(app.exec_())
