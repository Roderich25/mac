from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, label_binarize
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from itertools import cycle


# Count,3,0.5

def main():
    for folder in ["Count"]:
        for k in [3]:
            for ci, clf in enumerate([
                LogisticRegression(solver='lbfgs', multi_class='multinomial', penalty='l2', C=0.5, max_iter=10000),
                SVC(kernel='rbf', gamma=0.0001, C=1000, probability=True)]):
                denue_wide = pd.read_csv(f"summary/{folder}/denue_wide_{k}.csv")
                rezago = pd.read_csv("rezago_social/rezago_social.csv")
                rezago_social = rezago[["lgc00_15cl3", "Key", "POB_TOTAL"]]
                df = pd.merge(rezago_social, denue_wide, on=['Key'])
                df.drop(['Key'], axis=1, inplace=True)
                y = df['lgc00_15cl3']
                X = df.iloc[:, 2:].div((df.POB_TOTAL / 1000), axis=0)
                # X['pop'] = df.POB_TOTAL
                print(X.shape)
                X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.20, random_state=1)
                pipeline = make_pipeline(StandardScaler(), clf)
                scores = cross_val_score(pipeline, X_train, y_train, cv=10, n_jobs=-1)
                print(f"{clf}, cv='10', mean={np.mean(scores)}, median={np.median(scores)}, std={np.std(scores)}")
                scores = cross_val_score(pipeline, X_test, y_test, cv=5, n_jobs=-1)
                print(f"{clf}, cv='5', mean={np.mean(scores)}, median={np.median(scores)}, std={np.std(scores)}")

                # # Curva ROC
                # y_bin = label_binarize(y_test, classes=[1, 2, 3])
                # n_classes = y_bin.shape[1]
                # y_score = cross_val_predict(pipeline, X_test, y_test, cv=10, method='predict_proba')
                # fpr = dict()
                # tpr = dict()
                # roc_auc = dict()
                # for i in range(n_classes):
                #     fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], y_score[:, i])
                #     roc_auc[i] = auc(fpr[i], tpr[i])
                # colors = cycle(['blue', 'red', 'green'])
                # for i, color in zip(range(n_classes), colors):
                #     plt.plot(fpr[i], tpr[i], color=color, lw=2,
                #              label='ROC curve of class {0} (area = {1:0.6f})'
                #                    ''.format(i+1, roc_auc[i]))
                # plt.plot([0, 1], [0, 1], 'k--', lw=2)
                # plt.xlim([-0.05, 1.0])
                # plt.ylim([0.0, 1.05])
                # plt.xlabel('Tasa de Falsos Positivos')
                # plt.ylabel('Tasa de Verdaderos Positivos')
                # if ci == 0:
                #     plt.title(f"Regresión Logistica L2\nDENUE a nivel Subsector")
                # else:
                #     plt.title(f"Máquina de Soporte Vectorial, kernel RBF\nDENUE a nivel Subsector")
                # plt.legend(loc="lower right")
                # plt.show()


if __name__ == '__main__':
    main()
