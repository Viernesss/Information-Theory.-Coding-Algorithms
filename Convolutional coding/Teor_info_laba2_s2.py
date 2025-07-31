import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from l2s_2 import Ui_MainWindow
from bisect import bisect_left
from binarytree import Node


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.zakodir.clicked.connect(self.kodirovanie)
        self.ui.decodir.clicked.connect(self.dekodirovanie)


    def kodirovanie(self):
        text = self.ui.input_text.toPlainText()
        try:
            kol_razr = int(self.ui.kol_reg.text())
            summators = []
            for x in self.ui.summatorsss.toPlainText().split('\n'):
                summators.append([int(y) for y in x.split()])
        except:
            self.ui.output_cod.setText("Неверно введены сумматоры или количество регистров")
            return None
        if text != '':
            text = self.z_Haffman(text)
        else:
            self.ui.output_cod.setText("Введите текст")
            return None

        posled = [int(x) for x in text]
        sposob = self.ui.cmbb.currentText()
        if sposob == 'Регистры сдвига':
            self.diagram(kol_razr, summators, posled)
        elif sposob == 'Диаграмма состояний':
            self.graph(kol_razr, summators, posled)
        elif sposob == 'Древовидная диаграмма':
            self.derevo(kol_razr, summators, posled)
        elif sposob == 'Решётчатая диаграмма':
            self.reeshetka(kol_razr, summators, posled)
        elif sposob == 'Полиномиальное представление':
            self.polynom(kol_razr, summators, posled)


    def dekodirovanie(self, summators):
        text = self.ui.input_cod.toPlainText()
        try:
            kol_razr = int(self.ui.kol_reg.text())
            summators = []
            for x in self.ui.summatorsss.toPlainText().split('\n'):
                summators.append([int(y) for y in x.split()])
            print(kol_razr)
            print(summators)
        except:
            self.ui.output_cod.setText("Неверно введены сумматоры или количество регистров")
            return None
        print(text)
        flag = True
        for i in text:
            if i not in ['1', '0']:
                flag = False
        if text != '' and flag and (len(text) % len(summators) == 0):
            print(1234)
            text = self.decoder(kol_razr, summators, text)
            print(2345)
            self.d_Haffman(text)


    def progon_ch_summators(self, summators, sp_current):
        itog_posled = ''
        for j in range(len(summators)):
            ch_for_summators = []
            for x in range(len(summators[j])):
                ch_for_summators.append(sp_current[summators[j][x] - 1])
            itog_posled += str(self.sum_modul(ch_for_summators))
        return itog_posled


    def diagram(self, kol_razr, summators, posled):
        sp_current = [0 for x in range(kol_razr)]
        posled.reverse()
        itog_posled = ''
        for i in range(len(posled)):
            sp_current.pop()
            sp_current.insert(0, posled.pop())
            itog_posled += self.progon_ch_summators(summators, sp_current)
        self.ui.input_cod.setText(itog_posled)
        # print(itog_posled)


    def graph(self, kol_razr, summators, posled):
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
        print(d_vershin) # здесь выводится словарь, который хранит в себе некое представление графа
        itog_posled = ''
        current_str = '0' * (kol_razr - 1)
        for i in posled:
            itog_posled += d_vershin[current_str][i][0]
            current_str = d_vershin[current_str][i][1]
        self.ui.input_cod.setText(itog_posled)
        # print(itog_posled)


    def polynom(self, kol_razr, summators, posled):
        pol_i = []
        for i in range(len(posled)):
            if posled[i] == 1:
                pol_i.append(i)

        pol_g_summators = []
        for i in summators:
            pol_g = []
            for j in i:
                pol_g.append(j - 1)
            pol_g_summators.append(pol_g)

        pol_c_all = []
        for i in pol_g_summators:
            sp = []
            for j in pol_i:
                for x in i:
                    sp.append(x + j)
            pol_c = []
            for i in range(max(sp) + 1):
                if sp.count(i) % 2 != 0:
                    pol_c.append(i)
            pol_c_all.append(pol_c)

        pol_c = ['' for _ in range(len(posled))]
        for i in range(len(summators)):
            for j in range(len(posled)):
                if j in pol_c_all[i]:
                    pol_c[j] += '1'
                else:
                    pol_c[j] += '0'
        itog_posled = ''.join(pol_c)
        self.ui.input_cod.setText(itog_posled)
        # print(itog_posled)


    def reeshetka(self, kol_razr, summators, posled):
        sp_sootv = []
        cetka = [[{} for _ in range(len(posled) + 1)] for _ in range(2 ** (kol_razr - 1))]
        for i in range(2 ** (kol_razr - 1)):
            ver = str(bin(i))[2:]
            ver = '0' * ((kol_razr - 1) - len(ver)) + ver
            sp_sootv.append(ver)

        # заполнение сетки
        current_str = [0 for i in range(kol_razr - 1)]
        pred_sost = ''.join([str(x) for x in current_str])
        for i in range(len(posled)):
            if i == 0:
                cst1 = [0] + current_str
                cst2 = [1] + current_str
                ind1 = sp_sootv.index(''.join([str(cst1[x]) for x in range(len(cst1) - 1)]))
                ind2 = sp_sootv.index(''.join([str(cst2[x]) for x in range(len(cst2) - 1)]))
                cetka[ind1][i + 1][pred_sost] = ['0', self.progon_ch_summators(summators, cst1)]
                cetka[ind2][i + 1][pred_sost] = ['1', self.progon_ch_summators(summators, cst2)]
            else:
                for j in range(len(sp_sootv)):
                    if cetka[j][i]:
                        pred_sost = sp_sootv[j]
                        current_str = [int(x) for x in sp_sootv[j]]
                        cst1 = [0] + current_str
                        cst2 = [1] + current_str
                        ind1 = sp_sootv.index(''.join([str(cst1[x]) for x in range(len(cst1) - 1)]))
                        ind2 = sp_sootv.index(''.join([str(cst2[x]) for x in range(len(cst2) - 1)]))
                        cetka[ind1][i + 1][pred_sost] = ['0', self.progon_ch_summators(summators, cst1)]
                        cetka[ind2][i + 1][pred_sost] = ['1', self.progon_ch_summators(summators, cst2)]
        for x in cetka:
            for y in x:
                print("%-30s" % y, end=' ')
            print('\n')

        itog_posled = ''
        pred_sost = '0' * (kol_razr - 1)
        shag = 1
        for i in posled:
            current_str = str(i) + pred_sost[:(len(pred_sost) - 1)]
            ind = sp_sootv.index(current_str)
            itog_posled += cetka[ind][shag][pred_sost][1]
            pred_sost = current_str
            shag += 1
        self.ui.input_cod.setText(itog_posled)
        # print(itog_posled)


    def derevo(self, kol_razr, summators, posled):
        root = Node('Узел')
        sp_last = []
        sp_last.append(('0' * kol_razr, root))
        sp_current = []
        for _ in range(len(posled)):
            for i in range(len(sp_last)):
                node = sp_last[i][1]
                current_sost = sp_last[i][0]
                new_sost_left = [0] + [int(x) for x in current_sost[:(len(current_sost) - 1)]]
                new_sost_right = [1] + [int(x) for x in current_sost[:(len(current_sost) - 1)]]
                node.left = Node(self.progon_ch_summators(summators, new_sost_left))
                node.right = Node(self.progon_ch_summators(summators, new_sost_right))
                sp_current.append((new_sost_left, node.left))
                sp_current.append((new_sost_right, node.right))
            sp_last = sp_current.copy()
            sp_current = []
        print(root)

        itog_posled = ''
        current_node = root
        for i in posled:
            if i == 0:
                itog_posled += current_node.left.values[0]
                current_node = current_node.left
            else:
                itog_posled += current_node.right.values[0]
                current_node = current_node.right
        self.ui.input_cod.setText(itog_posled)
        # print(itog_posled)

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
        print(7654321)

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
        for x in cetka:
            for y in x:
                print("%-30s" % y, end=' ')
            print('\n')

        itog_posled = ''
        pred_sost = ''
        for i in range(len(zak_posled) // (kol_razr - 1), 0, -1):
            min_rasst = 12345678
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

    def sum_modul(self, sp):
        current = sp[0]
        for i in range(1, len(sp)):
            if (current == 0 and sp[i] == 0) or (current == 1 and sp[i] == 1):
                current = 0
            else:
                current = 1
        return current

    def z_Haffman(self, text):
        try:
            ver = []
            sp_zn = []
            text = text.lower()
            for i in text:
                if i not in sp_zn:
                    ver.append(1)
                    sp_zn.append(i)
                else:
                    ind = sp_zn.index(i)
                    ver[ind] += 1
            dl = len(text)
            ver = [x / dl for x in ver]
            for i in range(len(ver) - 1):
                for j in range(i + 1, len(sp_zn)):
                    if ver[i] < ver[j]:
                        ver[i], ver[j] = ver[j], ver[i]
                        sp_zn[i], sp_zn[j] = sp_zn[j], sp_zn[i]
            k = len(sp_zn)
            self.sl = {}
            for i in range(k - 1):
                summ = ver[-1] + ver[-2]
                ver = ver[:(len(ver) - 2)]
                ver.reverse()
                ind = bisect_left(ver, summ)
                ver.insert(ind, summ)
                ver.reverse()
                for i in sp_zn[-1]:
                    if i in self.sl:
                        self.sl[i] += '0'
                    else:
                        self.sl[i] = '0'
                for i in sp_zn[-2]:
                    if i in self.sl:
                        self.sl[i] += '1'
                    else:
                        self.sl[i] = '1'
                st = sp_zn[-1] + sp_zn[-2]
                sp_zn = sp_zn[:(len(sp_zn) - 2)]
                sp_zn.reverse()
                sp_zn.insert(ind, st)
                sp_zn.reverse()
            for k in self.sl.keys():
                self.sl[k] = self.sl[k][::-1]
            answer = ''
            for i in text:
                answer += self.sl[i]
            self.ui.output_cod.setText(answer)
            return answer

        except Exception as e:
            print(f"Произошла ошибка при открытии файла: {str(e)}")

    def d_Haffman(self, stroka):
        try:
            self.sl1 = {value: key for key, value in self.sl.items()}
            answer = ''
            current = ''
            for i in stroka:
                current += i
                if current in self.sl1:
                    answer += self.sl1[current]
                    current = ''
            self.ui.output_text.setText(answer)
        except:
            self.ui.output_text.setText("Введён неверный формат зашифрованного текста")


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
