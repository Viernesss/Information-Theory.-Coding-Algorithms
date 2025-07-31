import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from l3 import Ui_MainWindow
import math
import os
from bisect import bisect_left
import ast


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.vf.clicked.connect(self.otkr_f)
        self.ui.zh.clicked.connect(self.z_Haffman)
        self.ui.dh.clicked.connect(self.d_Haffman)
        self.ui.lz78.clicked.connect(self.LZ78)
        self.ui.lzw.clicked.connect(self.LZW)
        self.content = ''
        self.it = 0

    def otkr_f(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)")
        try:
            if filename:
                with open(filename, 'r', encoding="utf-8") as file:
                    self.content = file.read()
                    self.ui.tev.setText(self.content)
        except Exception as e:
            print(f"Произошла ошибка при открытии файла: {str(e)}")

    def z_Haffman(self):
        try:
            ver = []
            sp_zn = []
            self.content = self.content.lower()
            for i in self.content:
                if i not in sp_zn:
                    ver.append(1)
                    sp_zn.append(i)
                else:
                    ind = sp_zn.index(i)
                    ver[ind] += 1
            dl = len(self.content)
            ver = [x / dl for x in ver]
            for i in range(len(ver) - 1):
                for j in range(i + 1, len(sp_zn)):
                    if ver[i] < ver[j]:
                        ver[i], ver[j] = ver[j], ver[i]
                        sp_zn[i], sp_zn[j] = sp_zn[j], sp_zn[i]
            k = len(sp_zn)
            sl = {}
            for i in range(k - 1):
                summ = ver[-1] + ver[-2]
                ver = ver[:(len(ver) - 2)]
                ver.reverse()
                ind = bisect_left(ver, summ)
                ver.insert(ind, summ)
                ver.reverse()
                for i in sp_zn[-1]:
                    if i in sl:
                        sl[i] += '0'
                    else:
                        sl[i] = '0'
                for i in sp_zn[-2]:
                    if i in sl:
                        sl[i] += '1'
                    else:
                        sl[i] = '1'
                st = sp_zn[-1] + sp_zn[-2]
                sp_zn = sp_zn[:(len(sp_zn) - 2)]
                sp_zn.reverse()
                sp_zn.insert(ind, st)
                sp_zn.reverse()
            for k in sl.keys():
                sl[k] = sl[k][::-1]
            answer = str(sl) + "\n"
            for i in self.content:
                answer += sl[i]
            self.ui.tep.setText(answer)

            fname = "file" + str(self.it) + ".txt"
            f = open(fname, "w", encoding="utf-8")
            f.write(answer)
            self.it += 1
            # print(sl)

        except Exception as e:
            print(f"Произошла ошибка при открытии файла: {str(e)}")

    def d_Haffman(self):
        try:
            sl, stroka = self.content.split('\n')
            sl = ast.literal_eval(sl)
            sl1 = {value: key for key, value in sl.items()}
            answer = ''
            current = ''
            for i in stroka:
                current += i
                if current in sl1:
                    answer += sl1[current]
                    current = ''
            fname = "file" + str(self.it) + ".txt"
            f = open(fname, "w", encoding="utf-8")
            f.write(answer)
            self.it += 1
            self.ui.tep.setText(answer)
        except:
            self.ui.tep.setText("Введён неверный формат зашифрованного текста")
        # print(answer)
        # print(sl)
        # # sl = dict(sl)
        # print(stroka)

    def LZ78(self):
        try:
            answer = []
            current = ''
            sl = {}
            ind = 1
            pack = 0
            self.content = self.content.lower()
            for i in self.content:
                current += i
                if current not in sl:
                    if len(current) == 1:
                        pack = 0
                    answer.append((pack, i))
                    sl[current] = ind
                    ind += 1
                    current = ''
                else:
                    pack = sl[current]
            answer.append((pack, "@"))

            answer = list(map(str, answer))
            fname = "file" + str(self.it) + ".txt"
            f = open(fname, "w", encoding="utf-8")
            f.write('  '.join(answer))
            self.it += 1
            self.ui.tep.setText('  '.join(answer))
        except Exception as e:
            print(f"Произошла ошибка при открытии файла: {str(e)}")
        # print(answer)

    def LZW(self):
        try:
            fi = open("pr_rez.txt", "w", encoding="utf-8")
            self.content = self.content.lower()
            sp_zn = []
            for i in self.content:
                if i not in sp_zn:
                    sp_zn.append(i)
            sl = {x: sp_zn.index(x) for x in sp_zn}
            fi.write(str(sl) + '\n')
            sl1 = {}
            # print(sl)
            num = len(sl)
            current = self.content[0]
            cur_str = ''
            next = ''
            it_str = ''
            cur_str = current
            for i in self.content[1:]:
                next = i
                if (cur_str + next) not in sl:
                    sl[cur_str + next] = num
                    sl1[cur_str + next] = num
                    it_str += str(sl[cur_str])
                    fi.write(cur_str + next + ' ' + current + ' ' + next + ' ' + str(sl[cur_str]) + '\n')
                    num += 1
                    current = next
                    cur_str = current
                else:
                    fi.write(cur_str + next + ' ' + current + ' ' + next + ' -' + '\n')
                    current = next
                    cur_str += next
            fi.write(cur_str + '@ ' + current + ' @ ' + str(sl[cur_str]) + '\n')
            fi.write(str(sl1))
            fi.close()
            sl[cur_str + "@"] = num
            it_str += str(sl[cur_str])
            ist = str(sl) + '\n' + it_str
            fname = "file" + str(self.it) + ".txt"
            f = open(fname, "w", encoding="utf-8")
            f.write(ist)
            self.it += 1
            self.ui.tep.setText(ist)
        except Exception as e:
            self.ui.tep.setText("Произошла ошибка")
            # print(f"Произошла ошибка при открытии файла: {str(e)}")


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
