# coding=utf-8
import numpy as np
import math

'''     行列演算

    行列Aの逆行列
    A = np.linalg.inv(A)

    行列Aの転置行列
    A = A.T

    行列Aの行列式
    A = np.linalg.det(A)

    行列A,Bの和、差
    A + B
    A - B

    行列A、Bの乗算
    np.matmul(A,B)

'''


# ベイズ識別器クラス


class BayseClassifier:
    def __init__(self, sample, x):
        self.sample = sample
        self.x = x

    u = np.zeros(4)  # 平均ベクトルu
    s = np.zeros((4, 4))  # 共分散行列s

    # ベイズ推定を行うメソッド
    def BayesianInference(self):

        # 平均ベクトルuの推定をする関数
        def averagevector():
            u = np.zeros(4)
            for i in range(4):
                for j in range(self.sample):
                    u[i] += self.x[j][i]
                u[i] /= 50
            return u

        # 共分散行列sの推定をする関数
        def covariancematrix():
            s = np.zeros((4, 4))
            for j in range(self.sample):
                a = np.zeros((4, 4))
                b = np.zeros((4, 4))
                a[0] = self.x[j]
                a = a.T
                b[0] = self.u
                b = b.T
                s += np.matmul((a - b), (a - b).T)
            s /= self.sample - 1
            return s

        # 平均ベクトルの推定
        self.u = averagevector()
        # 共分散行列の推定
        self.s = covariancematrix()

    # 距離dを求めるメソッド
    def d(self, vector):

        # 距離dの計算
        det_s = np.linalg.det(self.s)  # 共分散行列の行列式
        d = np.matmul((vector - self.u).T, np.linalg.inv(self.s))
        d = np.matmul(d, (vector - self.u))
        d += math.log(det_s)
        return float(d)


# 任意のファイルからベクトルを入力する関数


def input_vector(filename):
    file = open(filename, 'r')
    x = np.zeros((4, 50), float)

    string = file.readline()
    listitem = string.split('\t')
    x[0] = list(map(float, listitem))

    string = file.readline()
    listitem = string.split('\t')
    x[1] = list(map(float, listitem))

    string = file.readline()
    listitem = string.split('\t')
    x[2] = list(map(float, listitem))

    string = file.readline()
    listitem = string.split('\t')
    x[3] = list(map(float, listitem))

    x = x.T
    file.close()
    return x


# 実行部
# 初期化
mixing_mat = np.zeros((3, 3))  # 混合行列
e = 0.0  # 誤識別率
iris = [0 for i in range(3)]  # インスタンス

# ファイルからサンプルを入力
setosa = input_vector("iris setosa.txt")
versicolor = input_vector("iris versicolor.txt")
viriginica = input_vector("iris virginica.txt")

# learn one out法でテスト
# setosaの中から1つずつ取り出しテストサンプルとしテストする
for i in range(50):
    # 訓練サンプルとテストサンプルの決定
    traningsample1 = setosa
    traningsample2 = versicolor
    traningsample3 = viriginica
    # testsample1の中から1つ取り出しテストサンプルにする
    testsample = traningsample1[i]
    traningsample1 = np.delete(traningsample1, [i], axis=0)

    # 訓練サンプルをベイズ識別に入力
    iris = [0 for i in range(3)]
    iris[0] = BayseClassifier(len(traningsample1), traningsample1)
    iris[1] = BayseClassifier(len(traningsample2), traningsample2)
    iris[2] = BayseClassifier(len(traningsample3), traningsample3)

    # 各クラスの共分散行列と平均ベクトルの推定
    for i in range(3):
        iris[i].BayesianInference()

    # クラスの識別
    # testsampleを使って距離dを計算
    ds = [iris[0].d(testsample), iris[1].d(testsample), iris[2].d(testsample)]

    # 混合行列に識別結果をカウント

    # 距離dの最小値がクラスsetosaの時
    if min(ds) == ds[0]:
        mixing_mat[0][0] += 1

    # 距離dの最小値がクラスversicolorの時
    elif min(ds) == ds[1]:
        mixing_mat[1][0] += 1

    # 距離dの最小値がクラスviriginicaの時
    elif min(ds) == ds[2]:
        mixing_mat[2][0] += 1

# versicolorの中から1つずつ取り出しテストサンプルにしテストする
for i in range(50):
    # 訓練サンプルとテストサンプルの決定
    traningsample1 = np.copy(setosa)
    traningsample2 = np.copy(versicolor)
    traningsample3 = np.copy(viriginica)
    # testsample2の中から1つ取り出しテストサンプルにする
    testsample = traningsample2[i]
    traningsample2 = np.delete(traningsample2, [i], axis=0)

    # 訓練サンプルをベイズ識別に入力
    iris = [0 for i in range(3)]
    iris[0] = BayseClassifier(len(traningsample1), traningsample1)
    iris[1] = BayseClassifier(len(traningsample2), traningsample2)
    iris[2] = BayseClassifier(len(traningsample3), traningsample3)

    # 各クラスの共分散行列と平均ベクトルの推定
    for i in range(3):
        iris[i].BayesianInference()

    # クラスの識別
    # testsampleを使って距離dを計算
    ds = [iris[0].d(testsample), iris[1].d(testsample), iris[2].d(testsample)]

    # 混合行列に識別結果をカウント

    # 距離dの最小値がクラスsetosaの時
    if (min(ds) == ds[0]):
        mixing_mat[0][1] += 1

    # 距離dの最小値がクラスversicolorの時
    elif min(ds) == ds[1]:
        mixing_mat[1][1] += 1

    # 距離dの最小値がクラスviriginicaの時
    elif min(ds) == ds[2]:
        mixing_mat[2][1] += 1

# viriginicaの中から1つずつ取り出しテストサンプルにしテストする
for i in range(50):
    # 訓練サンプルとテストサンプルの決定
    traningsample1 = setosa
    traningsample2 = versicolor
    traningsample3 = viriginica
    # testsample3の中から1つ取り出しテストサンプルにする
    testsample = traningsample3[i]
    traningsample3 = np.delete(traningsample3, [i], axis=0)

    # 訓練サンプルをベイズ識別に入力
    iris = [0 for i in range(3)]
    iris[0] = BayseClassifier(len(traningsample1), traningsample1)
    iris[1] = BayseClassifier(len(traningsample2), traningsample2)
    iris[2] = BayseClassifier(len(traningsample3), traningsample3)

    # 各クラスの共分散行列と平均ベクトルの推定
    for i in range(3):
        iris[i].BayesianInference()

    # クラスの識別
    # testsampleを使って距離dを計算
    ds = [iris[0].d(testsample), iris[1].d(testsample), iris[2].d(testsample)]

    # 混合行列に識別結果をカウント

    # 距離dの最小値がクラスsetosaの時
    if min(ds) == ds[0]:

        mixing_mat[0][2] += 1

    # 距離dの最小値がクラスversicolorの時
    elif min(ds) == ds[1]:
        mixing_mat[1][2] += 1

    # 距離dの最小値がクラスviriginicaの時
    elif min(ds) == ds[2]:

        mixing_mat[2][2] += 1


print(mixing_mat)
for i in range(3):
    e += mixing_mat[i][i]

e /= 150
e = 1 - e
print(e * 100)