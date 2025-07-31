import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from l3s2 import Ui_MainWindow
import os
from bisect import bisect_left
import re
from PIL import Image


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.open.clicked.connect(self.load_picture)
        self.ui.byteKod.clicked.connect(self.bytecode)
        self.ui.bloccoder.clicked.connect(self.blocCoder)
        self.ui.peremezh.clicked.connect(self.peremezhitel)
        self.ui.svertcoder.clicked.connect(self.svert_codir)
        self.ui.decoder.clicked.connect(self.decoderCoda)
        self.ui.enter.clicked.connect(self.saveElements)
        self.ui.punkt.clicked.connect(self.punkt2)
        self.answer = ''
        self.codeWords = []
        self.informWords = []
        self.n = 0
        self.k = 0
        self.dmin = 0
        self.pixel_matrix = []
        self.byteWords = []
        self.matrica_zak_bl = []
        self.new_matrix = []
        self.summators = []
        self.kol_razr = int()

    def load_picture(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.jpg);;All Files (*)")
        try:
            if filename:
                image = Image.open(filename)
                width, height = image.size
                self.pixel_matrix = []
                for y in range(height):
                    row = []
                    for x in range(width):
                        pixel = image.getpixel((x, y))
                        row.append(pixel[:3])
                    self.pixel_matrix.append(row)
                # ЗАГРУЗИТЬ ЭТО ЧУДО В ФАЙЛ
                for x in self.pixel_matrix:
                    print(x)
        except Exception as e:
            print(f"Произошла ошибка при открытии файла: {str(e)}")

    def bytecode(self):
        try:
            self.byteWords = []
            for x in range(len(self.pixel_matrix)):
                sp = []
                for y in self.pixel_matrix[x]:
                    # r, g, b = y[0], y[1], y[2]
                    infWord = ''
                    for i in range(len(y)):
                        a = str(bin(y[i]))[2:]
                        infWord += ("0" * (8 - len(a)) + a)
                    sp.append(infWord)
                self.byteWords.append(sp)
            # ТОЖЕ ЗАПИХНУТЬ В ФАЙЛ!!!!!
            for x in self.byteWords:
                print(x)
        except Exception as e:
            print(e)

        fname = "file_punkt2.txt"
        f = open(fname, "w", encoding="utf-8")
        text = ''
        for x in self.byteWords:
            text += ''.join(x)
        f.write(text)

    def blocCoder(self):
        try:
            self.matrica_zak_bl = []
            self.codeText = ''
            for x in self.byteWords:
                sp = []
                for y in x:
                    self.codeText = y
                    if len(self.codeText) % self.k != 0:
                        self.codeText = self.codeText + ("0" * (self.k - (len(self.codeText) % self.k)))
                    # print(self.codeText)
                    self.conn = {}
                    for i in range(len(self.informWords)):
                        self.conn[self.informWords[i]] = self.codeWords[i]

                    self.answer = ''
                    for i in range(0, len(self.codeText) - (self.k - 1), self.k):
                        self.answer += self.conn[self.codeText[i:(i + self.k)]]
                    sp.append(self.answer)
                self.matrica_zak_bl.append(sp)

            # ЗАПИСАТЬ В ФАЙЛ
            for x in self.matrica_zak_bl:
                print(x)

        except Exception as e:
            print(e)

    def peremezhitel(self):
        try:
            self.new_matrix = []
            for i in self.matrica_zak_bl:
                sp = []
                for x in range(len(i[0])):
                    slovo = ''
                    for y in range(len(i)):
                        slovo += i[y][x]
                    sp.append(slovo)
                self.new_matrix.append(sp)
                # print(new_matrix)

            # ЗАПИСАТЬ В ФАЙЛ
            for x in self.new_matrix:
                print(x)
        except Exception as e:
            print(e)

    def svert_codir(self):
        text = ''
        for x in self.new_matrix:
            for y in x:
                text += y

        try:
            self.kol_razr = int(self.ui.kol_reg.text())
            self.summators = []
            for x in self.ui.summatorsss.toPlainText().split('\n'):
                self.summators.append([int(y) for y in x.split()])
        except:
            self.ui.summatorsss.setText("Неверно введены сумматоры или количество регистров")
            return None

        print(text)
        posled = [int(x) for x in text]
        # print(posled)
        try:
            answer = self.graph(self.kol_razr, self.summators, posled)
        except Exception as e:
            print(e)
        fname = "file.txt"
        f = open(fname, "w", encoding="utf-8")
        f.write(answer)
        print(answer)
        print('------------------------------')

    def decoderCoda(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)")
        try:
            if filename:
                with open(filename, 'r', encoding="utf-8") as file:
                    cod = file.read()
        except Exception as e:
            print(f"Произошла ошибка при открытии файла: {str(e)}")

        for_peremezh = self.decoder(self.kol_razr, self.summators, cod)
        print(for_peremezh)

        for_bloc_coder = self.antiperemezhitel(for_peremezh)

        byte_decode_matrix = []
        for x in for_bloc_coder:
            sp = []
            for y in x:
                sp.append(self.encode_text(y))
            byte_decode_matrix.append(sp)
        # for x in byte_decode_matrix:
        #     print(x)

        answer = []
        for x in byte_decode_matrix:
            sp = []
            for y in x:
                r, g, b = int(y[0:8], 2), int(y[8:16], 2), int(y[16:24], 2)
                sp.append((r, g, b))
            answer.append(sp)
        for x in answer:
            print(x)

        try:
            for i in range(len(answer)):
                for j in range(len(answer[0])):
                    r, g, b = answer[i][j]
                    answer[i][j] = (r, g, b, 255)
            new_image = Image.new("RGBA", (len(answer[0]), len(answer)))
            for y in range(len(answer)):
                for x in range(len(answer[0])):
                    new_image.putpixel((x, y), tuple(answer[y][x]))
            new_image.save("new_image.png")
        except Exception as e:
            print(e)

    def saveElements(self):
        try:
            matrix = self.ui.teM.toPlainText().split("\n")
            if matrix == "":
                self.ui.teM.setText("Введите матрицу")
                return None
            elif len(matrix) == len(matrix[0]):
                self.ui.teM.setText("Матрица введена неверно, попробуйте ещё раз")
                return None
            else:
                dl = len(matrix[0])
                for i in matrix:
                    if len(i) != dl:
                        self.ui.teM.setText("Матрица введена неверно, попробуйте ещё раз")
                        return None
            for i in matrix:
                for j in i:
                    if j not in ['1', '0']:
                        self.ui.teM.setText("Матрица состоит не из 0 и 1. Повторите ввод")
                        return None
            matrG, matrH = self.findMatrix(matrix)
            if matrH == None:
                return None

            self.k = len(matrG)
            self.n = len(matrG[0])
            # self.informWords = []
            # self.codeWords = []

            for i in range(2 ** self.k):
                word = str(bin(i))[2:]
                self.informWords.append("0" * (self.k - len(word)) + word)
            for i in range(len(self.informWords)):
                forOperation = []
                for j in range(len(self.informWords[i])):
                    if self.informWords[i][j] == "1":
                        forOperation.append(matrG[j])
                if forOperation != []:
                    self.codeWords.append(self.xxor(forOperation))
                else:
                    self.codeWords.append("0" * len(matrG[0]))
            distanceHamm = []
            text = ""
            for i in range(len(self.informWords)):
                text += self.informWords[i] + "  " + self.codeWords[i] + "\n"
                ch = self.codeWords[i].count("1")
                if ch != 0:
                    distanceHamm.append(ch)
            self.dmin = min(distanceHamm)
            self.r = self.dmin - 1
            self.t = (self.dmin - 1) // 2
            self.matrHT = self.transp(matrH)

            self.e = []
            self.S = []
            self.e.append("0" * len(self.matrHT))
            for i in range(2 ** self.n):
                st = str(bin(i))[2:]
                if st.count("1") == self.t:
                    self.e.append("0" * (self.n - len(st)) + st)
            for i in range(len(self.e)):
                forOperation = []
                for j in range(len(self.e[i])):
                    if self.e[i][j] == "1":
                        forOperation.append(self.matrHT[j])
                if forOperation != []:
                    self.S.append(self.xxor(forOperation))
                else:
                    self.S.append("0" * len(self.matrHT[0]))
            text = ''
            self.sindromVector = {}
            for i in range(len(self.e)):
                text += self.S[i] + "  " + self.e[i] + "\n"
                self.sindromVector[self.S[i]] = self.e[i]
        except Exception as e:
            print(e)

    def findMatrix(self, matrix):
        if self.ui.rH.isChecked():
            matrix = self.transp(matrix)
            for i in range(len(matrix)):
                if matrix[i].count("1") == 1:
                    ind = matrix[i].index("1")
                    el = matrix[i]
                    matrix.remove(el)
                    matrix.insert(ind, el)
            matrix = self.transp(matrix)
            for i in range(len(matrix)):
                matrix[i] = matrix[i][len(matrix):] + matrix[i][:len(matrix)]
            matrH = matrix.copy()
            matrG = []
            for i in range(len(matrix)):
                matrG.append(matrix[i][:(len(matrix) + 1)])
            matrG = self.transp(matrG)
            for i in range(len(matrG)):
                sp = ["0"] * len(matrG)
                sp[i] = "1"
                matrG[i] = "".join(sp) + matrG[i]
            text = "\n".join(matrG)
            self.ui.teaM.setText(text)
        elif self.ui.rG.isChecked():
            matrix = self.transp(matrix)
            for i in range(len(matrix)):
                if matrix[i].count("1") == 1:
                    ind = matrix[i].index("1")
                    matrix[i], matrix[ind] = matrix[ind], matrix[i]
            matrix = self.transp(matrix)
            matrG = matrix.copy()
            matrH = []
            for i in range(len(matrG)):
                matrH.append(matrG[i][len(matrG):])
            matrH = self.transp(matrH)
            for i in range(len(matrH)):
                sp = ["0"] * len(matrH)
                sp[i] = "1"
                matrH[i] = matrH[i] + "".join(sp)
            text = "\n".join(matrH)
            self.ui.teaM.setText(text)
        else:
            self.ui.teaM.setText("Не выбран тип матрицы")
            return None, None
        text = "\n".join(matrix)
        self.ui.teM.setText(text)
        return matrG, matrH

    def xxor(self, array):
        current = array[0]
        for i in range(1, len(array)):
            next = array[i]
            newString = ''
            for j in range(len(current)):
                if (next[j] == "1" and current[j]) == "1":
                    newString += "0"
                elif (next[j] == "0" and current[j]) == "0":
                    newString += "0"
                else:
                    newString += "1"
            current = newString
        return current

    def transp(self, matrix):
        m1 = []
        for i in range(len(matrix[0])):
            st = ''
            for j in range(len(matrix)):
                st += matrix[j][i]
            m1.append(st)
        return m1

    def graph(self, kol_razr, summators, posled):
        try:
            d_vershin = {}
            for i in range(2 ** (kol_razr - 1)):
                ver = str(bin(i))[2:]
                ver = '0' * ((kol_razr - 1) - len(ver)) + ver
                ver_spiskom = []
                for j in ver:
                    ver_spiskom.append(int(j))
                d_vershin[ver] = []
                d_vershin[ver].append([self.progon_ch_summators(summators, [0] + ver_spiskom),
                                       ''.join(['0'] + [str(x) for x in ver_spiskom[:(len(ver_spiskom) - 1)]])])
                d_vershin[ver].append([self.progon_ch_summators(summators, [1] + ver_spiskom),
                                       ''.join(['1'] + [str(x) for x in ver_spiskom[:(len(ver_spiskom) - 1)]])])
            # print(d_vershin) # здесь выводится словарь, который хранит в себе некое представление графа
            itog_posled = ''
            current_str = '0' * (kol_razr - 1)
            for i in posled:
                itog_posled += d_vershin[current_str][i][0]
                current_str = d_vershin[current_str][i][1]
            return itog_posled
        except Exception as e:
            print(e)

    def progon_ch_summators(self, summators, sp_current):
        try:
            itog_posled = ''
            for j in range(len(summators)):
                ch_for_summators = []
                for x in range(len(summators[j])):
                    ch_for_summators.append(sp_current[summators[j][x] - 1])
                itog_posled += str(self.sum_modul(ch_for_summators))
            return itog_posled
        except Exception as e:
            print(e)

    def sum_modul(self, sp):
        try:
            current = sp[0]
            for i in range(1, len(sp)):
                if (current == 0 and sp[i] == 0) or (current == 1 and sp[i] == 1):
                    current = 0
                else:
                    current = 1
            return current
        except Exception as e:
            print(e)

    def rasst_h(self, st1, st2):
        rasst = 0
        sp1 = [int(x) for x in st1]
        sp2 = [int(x) for x in st2]
        for i in range(len(sp1)):
            if sp1[i] != sp2[i]:
                rasst += 1
        return str(rasst)

    def decoder(self, kol_razr, summators, zak_posled):
        sp_sootv = []
        cetka = [[{} for _ in range(len(zak_posled) // (kol_razr - 1) + 1)] for _ in range(2 ** (kol_razr - 1))]
        for i in range(2 ** (kol_razr - 1)):
            ver = str(bin(i))[2:]
            ver = '0' * ((kol_razr - 1) - len(ver)) + ver
            sp_sootv.append(ver)

        # заполнение сетки
        current_str = [0 for i in range(kol_razr - 1)]
        pred_sost = ''.join([str(x) for x in current_str])
        pred_sum = 0
        interval = len(summators)
        shag = 0
        for i in range(len(zak_posled) // (kol_razr - 1)):
            if i == 0:
                cst1 = [0] + current_str
                cst2 = [1] + current_str
                ind1 = sp_sootv.index(''.join([str(cst1[x]) for x in range(len(cst1) - 1)]))
                ind2 = sp_sootv.index(''.join([str(cst2[x]) for x in range(len(cst2) - 1)]))
                pcs1 = self.progon_ch_summators(summators, cst1)
                pcs2 = self.progon_ch_summators(summators, cst2)
                rasst1 = self.rasst_h(pcs1, zak_posled[shag:(shag + interval)])
                rasst2 = self.rasst_h(pcs2, zak_posled[shag:(shag + interval)])
                current_sum1 = str(int(rasst1) + int(pred_sum))
                current_sum2 = str(int(rasst2) + int(pred_sum))
                cetka[ind1][i + 1][pred_sost] = ['0', pcs1, rasst1, current_sum1]
                cetka[ind2][i + 1][pred_sost] = ['1', pcs2, rasst2, current_sum2]
            else:
                for j in range(len(sp_sootv)):
                    if cetka[j][i]:
                        pred_sost = sp_sootv[j]
                        current_str = [int(x) for x in sp_sootv[j]]
                        pred_sum = str(min([int(x[3]) for x in cetka[j][i].values()]))
                        cst1 = [0] + current_str
                        cst2 = [1] + current_str
                        ind1 = sp_sootv.index(''.join([str(cst1[x]) for x in range(len(cst1) - 1)]))
                        ind2 = sp_sootv.index(''.join([str(cst2[x]) for x in range(len(cst2) - 1)]))
                        pcs1 = self.progon_ch_summators(summators, cst1)
                        pcs2 = self.progon_ch_summators(summators, cst2)
                        rasst1 = self.rasst_h(pcs1, zak_posled[shag:(shag + interval)])
                        rasst2 = self.rasst_h(pcs2, zak_posled[shag:(shag + interval)])
                        current_sum1 = str(int(rasst1) + int(pred_sum))
                        current_sum2 = str(int(rasst2) + int(pred_sum))
                        cetka[ind1][i + 1][pred_sost] = ['0', pcs1, rasst1, current_sum1]
                        cetka[ind2][i + 1][pred_sost] = ['1', pcs2, rasst2, current_sum2]
            shag += interval
        # for x in cetka:
        #     for y in x:
        #         print("%-30s" % y, end=' ')
        #     print('\n')

        itog_posled = ''
        pred_sost = ''
        for i in range(len(zak_posled) // (kol_razr - 1), 0, -1):
            min_rasst = 12345678987654
            ind = 0
            if i == len(zak_posled) // (kol_razr - 1):
                for j in range(len(sp_sootv)):
                    for key, values in cetka[j][i].items():
                        if int(values[3]) < min_rasst:
                            min_rasst = int(values[3])
                            pred_sost = key
                            ind = j
            else:
                ind = sp_sootv.index(pred_sost)
                for key, values in cetka[ind][i].items():
                    if int(values[3]) < min_rasst:
                        min_rasst = int(values[3])
                        pred_sost = key
            itog_posled = cetka[ind][i][pred_sost][0] + itog_posled
        # print(itog_posled)
        return itog_posled

    def antiperemezhitel(self, text):
        kol_el = 24 // self.k * self.n
        matr_per = []
        ind = 0
        for i in range(len(self.pixel_matrix)):
            counter = 0
            sp = []
            while counter != kol_el:
                sp.append(text[ind:(ind + len(self.pixel_matrix[0]))])
                ind += len(self.pixel_matrix[0])
                counter += 1
            matr_per.append(sp)

        for x in matr_per:
            print(x)

        matrix = []
        for x in matr_per:
            sp = []
            for i in range(len(x[0])):
                slovo = ''
                for j in range(len(x)):
                    slovo += x[j][i]
                sp.append(slovo)
            matrix.append(sp)
        for x in matrix:
            print(x)

        return matrix

    def encode_text(self, text):
        try:
            encodeCode = ''
            self.conn_obr = {v: k for k, v in self.conn.items()}
            for i in range(0, len(text) - (self.n - 1), self.n):
                stroka = text[i:(i + self.n)]
                sp = []
                for j in range(len(stroka)):
                    if stroka[j] == "1":
                        sp.append(self.matrHT[j])
                if sp:
                    s = self.xxor(sp)
                else:
                    s = "0" * len(self.matrHT[0])
                c = self.sindromVector[s]
                if s.count("1") == 0:
                    encodeCode += self.conn_obr[stroka]
                else:
                    sp = []
                    sp.append(c)
                    sp.append(stroka)
                    cs = self.xxor(sp)
                    if cs in self.conn_obr:
                        encodeCode += self.conn_obr[cs]
                    else:
                        encodeCode += "?" * self.k
            return encodeCode
        except Exception as e:
            print(e)

    def punkt2(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)")
        try:
            if filename:
                with open(filename, 'r', encoding="utf-8") as file:
                    text = file.read()
        except Exception as e:
            print(f"Произошла ошибка при открытии файла: {str(e)}")
        print(text)

        text_sp = []
        ind = 0
        for i in range(len(self.pixel_matrix)):
            sp = []
            for j in range(len(self.pixel_matrix[0])):
                sp.append(text[ind:(ind + 24)])
                ind += 24
            text_sp.append(sp)
        # print(text_sp)

        answer = []
        for x in text_sp:
            sp = []
            for y in x:
                r, g, b = int(y[0:8], 2), int(y[8:16], 2), int(y[16:24], 2)
                sp.append((r, g, b))
            answer.append(sp)
        for x in answer:
            print(x)

        try:
            for i in range(len(answer)):
                for j in range(len(answer[0])):
                    r, g, b = answer[i][j]
                    answer[i][j] = (r, g, b, 255)
            new_image = Image.new("RGBA", (len(answer[0]), len(answer)))
            for y in range(len(answer)):
                for x in range(len(answer[0])):
                    new_image.putpixel((x, y), tuple(answer[y][x]))
            new_image.save("new_image_punkt2.png")
        except Exception as e:
            print(e)


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())

# 1001001
# 0110001
# 0101100
# 0101011
