#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.core.window import Window
from kivy.app import App, platform
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.filebrowser import FileBrowser
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout

import sys
from time import time
from os.path import dirname, expanduser, sep

from pathlib2 import Path
from numpy.random import sample, randint
import matplotlib
from matplotlib import mlab

matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

import matplotlib.pyplot as plt

from Matrix import Matrix

path_file = 'matrix.txt'
cool_thread = 4
sys.setrecursionlimit(3000)



def pars_input(s):
    a = []
    b = []
    for i in s.split('\n'):
        if i == '':
            break
        ai = []
        k = i.split()
        for j in range(len(k) - 1):
            ai.append(float(k[j]))
        a.append(ai)
        b.append(float(k[-1]))
    n = len(b)
    return n, a, b


def plot(x, y, title, xlabel, ylabel, t):
    fig, ax = plt.subplots()
    fig.suptitle(title, fontsize=20, fontweight='bold')
    ax.plot(x, y, 'r-', label=u"Метод Якоби")
    ax.set_xlabel(xlabel, fontsize=14)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    ax.set_ylabel(ylabel, fontsize=14)
    if t: ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    c = fig.canvas
    fl = BoxLayout(orientation="vertical")
    fl.add_widget(c)
    return fl


def plot_time_threads(n, a, b):
    y_time = []
    x_threads = [i for i in range(1, 15)]
    for num_t in x_threads:
        eps = 0.0001
        l = sample(20)
        for _ in range(20):
            m = Matrix(n, a, b, eps, num_t)
            t = time()
            m.methodJacobiPrallel()
            l[_] = time() - t
        y_time.append(l.mean())
    cool_thread = x_threads[y_time.index(min(y_time))]
    print cool_thread
    return plot(x_threads, y_time, u'Время от нитей', u'Нити', u'Время', 0)


def plot_time_eps(n, a, b):
    x_eps = [10 ** (-i) for i in reversed(range(3, 7))]
    y_time = []
    for eps in x_eps:
        num_t = cool_thread
        l = sample(20)
        for _ in range(20):
            m = Matrix(n, a, b, eps, num_t)
            t = time()
            m.methodJacobiPrallel()
            l[_] = time() - t
        y_time.append(l.mean())
    print x_eps[y_time.index(min(y_time))]
    return plot(x_eps, y_time, u'Время от эписилон', u'Эпсилон', u'Время', 0)


def plot_time_msize():
    x_n = mlab.frange(1, 1001, 100)
    y_time = []
    x_n2 = []
    y_time2 = []
    for n in x_n:
        print n
        a = sample((n, n))
        b = sample(n)
        a * 100
        b * 100
        a = list(a)
        b = list(b)
        l = sample(20)
        for _ in range(20):
            m = Matrix(n, a, b, 0.0001, cool_thread)
            t = time()
            m.methodJacobiPrallel()
            l[_] = time() - t
        y_time.append(l.mean())
        if n < 500:
            l = sample(20)
            for _ in range(20):
                m = Matrix(n, a, b, 0.00001, cool_thread)
                t = time()
                m.methodGaus()
                l[_] = time() - t
            x_n2.append(n)
            y_time2.append(l.mean())
        print y_time[-1], y_time2[-1]

    print y_time, y_time2
    fig, ax = plt.subplots()
    fig.suptitle(u'Время от размера матрицы', fontsize=20, fontweight='bold')
    ax.plot(x_n, y_time, 'r-', label=u"Метод Якоби")
    ax.plot(x_n2, y_time2, 'b-', label=u"Метод Гауса")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set_xlabel(u'Размер Матрицы', fontsize=14)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    ax.set_ylabel(u'Время', fontsize=14)
    # ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    c = fig.canvas
    fl = BoxLayout(orientation="vertical")
    fl.add_widget(c)
    return fl


class ScreenManagement(ScreenManager):
    pass


class Controller(Screen, FloatLayout):
    answer = StringProperty()
    matrix = ObjectProperty(None)
    template = StringProperty()
    gaus = ObjectProperty()
    jacobi = ObjectProperty()
    calc = ObjectProperty()
    gen = ObjectProperty()
    gr = ObjectProperty()
    carousel = ObjectProperty()

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self.template = u'Введите матрицу формата:\n a11 a12 a13 b1\n a21 a22 a23 b2\n a31 a32 a33 b2'
        self.num = 0

    def calculate(self):
        text = self.matrix.text
        try:
            f = open(path_file)
            self.num = len(f.readline().split()) - 1
            f.close()
        except:
            f = open(path_file, 'w')
            f.close()
        if self.matrix.text == '':
            if path_file != 'matrix.txt':
                text = Path(path_file).read_text()
            else:
                f = open(path_file)
                for i in range(self.num):
                    text += f.readline()
        n, a, b = pars_input(text)
        m = Matrix(n, a, b, 0.0001, 4)
        if self.gaus.active:
            m.methodGaus()
        else:
            m.methodJacobiPrallel()
        answer = m.getAnswer()
        self.answer = ' '.join(['x' + str(i) + '=' + str(answer[i]) for i in range(len(answer))])

    def default_file(self):
        path_file = 'matrix.txt'

    def generate(self):
        f = open('matrix.txt', 'w')
        path_file = 'matrix.txt'
        n = randint(100)
        self.num = n
        print(self.num)
        l = sample((n, n + 1))
        l * 100
        for i in range(len(l)):
            l[i][i] = 200 * n
        for i in range(n):
            f.write(' '.join([str(l[i][j]) for j in range(n)]) + ' ' + str(l[i][-1]) + '\n')

    def graphs(self):
        n = randint(100, 500)
        # n = 4
        print(n)
        a = sample((n, n))
        b = sample(n)
        a * 100
        b * 100
        a = list(a)
        b = list(b)

        self.carousel.add_widget(plot_time_threads(n, a, b))

        self.carousel.add_widget(plot_time_eps(n, a, b))

        self.carousel.add_widget(plot_time_msize())


class FileOpen(Screen, FileBrowser):
    if platform == 'win':
        user_path = dirname(expanduser('~')) + sep + 'Documents'
    else:
        user_path = expanduser('~') + sep + 'Documents'

    def __init__(self, **kwargs):
        super(FileOpen, self).__init__(select_string='Select', favorites=[(self.user_path, 'Documents')], **kwargs)
        self.bind(
            on_success=self._fbrowser_success,
            on_canceled=self._fbrowser_canceled)

    def _fbrowser_canceled(self, instance):
        self.parent.current = 'controller'
        path_file = 'matrix.txt'

    def _fbrowser_success(self, instance):
        self.parent.current = 'controller'
        path_file = instance.selection[0].encode('utf8')


presentation = Builder.load_file("controller.kv")


class ControllerApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1200, 700)
        self.title = "Matrix"
        return presentation


if __name__ == '__main__':
    ControllerApp().run()
