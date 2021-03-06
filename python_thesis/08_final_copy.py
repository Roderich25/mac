from matplotlib.lines import Line2D
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, classification_report, plot_roc_curve, precision_recall_curve, \
    average_precision_score
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, label_binarize
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, font_manager
from itertools import cycle
import geopandas as gpd
import matplotlib
import mord
import seaborn as sns
import scikitplot as skplt

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams["font.weight"] = "bold"
matplotlib.rcParams["axes.labelweight"] = "bold"


def plot_multiclass_roc(clf, X_test, y_test, n_classes, figsize=(17, 6)):
    y_score = clf.predict_proba(X_test)

    # structures
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    # calculate dummies once
    y_test_dummies = pd.get_dummies(y_test, drop_first=False).values
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_dummies[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # roc for each class
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver operating characteristic example')
    for i in range(n_classes):
        ax.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f) for label %i' % (roc_auc[i], i))
    ax.legend(loc="best")
    ax.grid(alpha=.4)
    sns.despine()
    plt.show()


def main_clf(metric_, clf_, grid_, range_=(2, 7), cv_=5, verb_=False, graphs=False):
    pipe = Pipeline(steps=[('sc', StandardScaler()), ('clf', clf_)])
    max_scoring = 0
    for k in range(*range_):
        denue_wide = pd.read_csv(f"summary/Count/denue_wide_{k}.csv")  ###
        rezago = pd.read_csv("rezago_social/rezago_social.csv")
        rezago_social = rezago[["lgc00_15cl3", "Key", "POB_TOTAL", "LAT", "LON"]]
        df = pd.merge(rezago_social, denue_wide, on=['Key'])
        y = rezago_social['lgc00_15cl3']
        df.drop(["lgc00_15cl3", "Key", "LAT", "LON"], axis=1, inplace=True)
        X = df.div(df.POB_TOTAL, axis=0) * 1000
        X.drop(["POB_TOTAL"], axis=1, inplace=True)
        X["LAT"] = rezago_social["LAT"]
        X["LON"] = rezago_social["LON"]
        print(f'# CLF {k} {X.shape}')
        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.20, random_state=0)
        clf_cv = GridSearchCV(pipe, grid_, cv=10, scoring=metric_, verbose=verb_)  # cv_
        clf_cv.fit(X_train, y_train)
        if np.mean(clf_cv.best_score_) > max_scoring:
            max_scoring = clf_cv.best_score_
            print(f"\t # {k} CLF {clf_cv.best_score_} {clf_cv.best_params_}")
            best_params = clf_cv.best_params_
            best_k = k
            Xtrain, ytrain = X_train, y_train
            Xtest, ytest = X_test, y_test
            X_, y_ = X, y
    best_params_ = {k[5:]: v for k, v in best_params.items()}
    best_clf = clf_.set_params(**best_params_)
    best_pipe = Pipeline(steps=[('sc', StandardScaler()), ('clf', best_clf)])
    print('#BEST', best_pipe, max_scoring)
    best_pipe.fit(Xtrain, ytrain)
    print(f"# {best_k}: Train:{best_pipe.score(Xtrain, ytrain) * 100}")
    print(f"# {best_k}: Test:{best_pipe.score(Xtest, ytest) * 100}")
    scores = cross_val_score(best_pipe, X_, y_, cv=cv_, n_jobs=-1, scoring='accuracy')
    print(f"# {best_k}: Accuracy CV5:{np.mean(scores)} +/- {np.std(scores)}")
    scores_ = cross_val_score(best_pipe, X_, y_, cv=cv_, n_jobs=-1, scoring=metric_)
    print(f"# {best_k}: {metric_} CV5:{np.mean(scores_)} +/- {np.std(scores_)}")
    y_pred = cross_val_predict(best_pipe, X_, y_, cv=cv_)
    print(classification_report(y_, y_pred, digits=3))

    # plot_multiclass_roc(best_pipe, X_, y_, n_classes=3, figsize=(16, 10))
    probas = cross_val_predict(best_pipe, X_, y_, cv=cv_, method='predict_proba')
    fig, (ax1, ax2) = plt.subplots(1, 2)
    skplt.metrics.plot_roc(y_, probas, ax=ax1, title='')
    handles, labels = ax1.get_legend_handles_labels()
    print(labels)
    labels = [lb.replace(' 1 ', ' B ').replace(' 2 ', ' M ').replace(' 3 ', ' A ') for lb in labels]
    print(labels)
    ax1.legend(handles, labels)
    ax1.get_figure()
    ax1.set_xlabel('TFP\n(A)')
    skplt.metrics.plot_precision_recall(y_, probas, ax=ax2, title='')
    handles, labels = ax2.get_legend_handles_labels()
    print(labels)
    labels = [lb.replace(' 1 ', ' B ').replace(' 2 ', ' M ').replace(' 3 ', ' A ') for lb in labels]
    print(labels)
    ax2.legend(handles, labels)
    ax2.get_figure()
    ax2.set_xlabel('S\n(B)')
    plt.show()

    if graphs:
        ###
        denue_2016 = pd.read_csv(f"summary/201610/denue_wide_{best_k}.csv")  ###
        df_2016 = pd.merge(rezago_social, denue_2016, on=['Key'])
        df_2016.drop(["lgc00_15cl3", "Key", "LAT", "LON"], axis=1, inplace=True)
        X_2016 = df.div(df.POB_TOTAL, axis=0) * 1000
        X_2016.drop(["POB_TOTAL"], axis=1, inplace=True)
        X_2016["LAT"] = rezago_social["LAT"]
        X_2016["LON"] = rezago_social["LON"]
        y_pred_2016 = best_pipe.predict(X_2016)
        ###
        denue_2017 = pd.read_csv(f"summary/201711/denue_wide_{best_k}.csv")  ###
        df_2017 = pd.merge(rezago_social, denue_2017, on=['Key'])
        df_2017.drop(["lgc00_15cl3", "Key", "LAT", "LON"], axis=1, inplace=True)
        X_2017 = df.div(df.POB_TOTAL, axis=0) * 1000
        X_2017.drop(["POB_TOTAL"], axis=1, inplace=True)
        X_2017["LAT"] = rezago_social["LAT"]
        X_2017["LON"] = rezago_social["LON"]
        y_pred_2017 = best_pipe.predict(X_2017)
        # Confusion matrix
        skplt.metrics.plot_confusion_matrix(y_, y_pred, normalize=True, title=" ")
        plt.xticks([0, 1, 2], ['B', 'M', 'A'], rotation='horizontal')
        plt.yticks([0, 1, 2], ['B', 'M', 'A'], rotation='horizontal')
        plt.xlabel('Clases predichas')
        plt.ylabel('Clases verdaderas')
        plt.show()
        # Mapa
        rezago_social['Pred'] = y_pred
        rezago_social['Pred_2016'] = y_pred_2016
        rezago_social['Pred_2017'] = y_pred_2017
        print("Rodrigo:",
              rezago_social['Pred_2016'].equals(rezago_social['Pred_2016']),
              rezago_social['Pred_2017'].equals(rezago_social['Pred_2017']),
              rezago_social['Pred_2017'].equals(rezago_social['Pred_2016']),
              rezago_social['Pred_2016'].equals(rezago_social['Pred_2017']))
        rezago_social['Key_'] = rezago_social['Key'].astype(str).str.zfill(5)
        gdf = gpd.read_file('municipios/areas_geoestadisticas_municipales.shp')
        gdf['Key_'] = gdf['CVE_ENT'] + gdf['CVE_MUN']
        gdf = gdf.merge(rezago_social, on='Key_')
        legend_elements = [Line2D([0], [0], marker='o', color='w', label='A',
                                  markerfacecolor='r', markersize=10, ),
                           Line2D([0], [0], marker='o', color='w', label='M',
                                  markerfacecolor='yellow', markersize=10),
                           Line2D([0], [0], marker='o', color='w', label='B',
                                  markerfacecolor='g', markersize=10)]
        csfont = {'fontname': 'Times New Roman'}
        font = font_manager.FontProperties(family='Times New Roman', weight='normal', style='normal', size=12)
        colors = {1: 'green', 2: 'yellow', 3: 'red'}
        models = {'RandomForestClassifier': 'RF', 'SCV': 'SVM', 'LogisticRegression': 'LR'}
        ###
        # gdf.plot(color=gdf['Pred_2016'].map(colors))
        # plt.xticks([])
        # plt.yticks([])
        # txt = f"Categorías predichas por modelo {models.get(clf.__class__.__name__, 'ABC')}, para el año 201X."
        # plt.text(800000, 0.01, txt, wrap=True, horizontalalignment='left', fontsize=12, **csfont)
        # plt.legend(handles=legend_elements, prop=font)
        # plt.show()
        ### Mapa
        fig, (ax1, ax2) = plt.subplots(1, 2)
        gdf.plot(ax=ax1, color=gdf['Pred_2016'].map(colors))
        ax1.set_xticks([])
        ax1.set_yticks([])
        txt = f"(A) Clases predichas con modelo {models.get(clf.__class__.__name__, 'ABC')} en 2016"
        ax1.text(800000, 0.01, txt, wrap=True, horizontalalignment='left', fontsize=12, **csfont)
        ax1.legend(handles=legend_elements, prop=font)
        gdf.plot(ax=ax2, color=gdf['Pred_2017'].map(colors))
        ax2.set_xticks([])
        ax2.set_yticks([])
        txt = f"(B) Clases predichas con modelo {models.get(clf.__class__.__name__, 'ABC')} en 2017"
        ax2.text(800000, 0.01, txt, wrap=True, horizontalalignment='left', fontsize=12, **csfont)
        ax2.legend(handles=legend_elements, prop=font)
        plt.show()

        ### Mapa
        fig, (ax1, ax2) = plt.subplots(1, 2)
        gdf.plot(ax=ax1, color=gdf['lgc00_15cl3'].map(colors), legend=True)
        ax1.set_xticks([])
        ax1.set_yticks([])
        txt = "(A) Clases de acuerdo a Valdés-Cruz y Vargas-Chanes (2017)"
        ax1.text(800000, 0.01, txt, wrap=True, horizontalalignment='left', fontsize=12, **csfont)
        ax1.legend(handles=legend_elements, prop=font)
        gdf.plot(ax=ax2, color=gdf['Pred'].map(colors))
        ax2.set_xticks([])
        ax2.set_yticks([])
        txt = f"(B) Clases predichas con modelo {models.get(clf.__class__.__name__, 'ABC')} en 2015"
        ax2.text(800000, 0.01, txt, wrap=True, horizontalalignment='left', fontsize=12, **csfont)
        ax2.legend(handles=legend_elements, prop=font)
        plt.show()
        # Curva ROC
        y_bin = label_binarize(y, classes=[1, 2, 3])
        n_classes = y_bin.shape[1]
        y_score = cross_val_predict(best_pipe, X_, y_, cv=cv_, method='predict_proba')
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
        mean_tpr /= n_classes
        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
        plt.figure()
        plt.plot(fpr["macro"], tpr["macro"],
                 label='ROC macro (AUC = {0:0.3f})'
                       ''.format(roc_auc["macro"]),
                 color='navy', linestyle=':', linewidth=4)
        rezago = {1: 'B', 2: 'M', 3: 'A'}
        colors = cycle(['green', 'yellow', 'red'])
        for i, color in zip(range(n_classes), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=2,
                     label='Clase de rezago {0} (AUC = {1:0.3f})'
                           ''.format(rezago[i + 1], roc_auc[i]))
        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([-0.05, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('TFP', fontsize=12, **csfont)
        plt.ylabel('TVP', fontsize=12, **csfont)
        plt.legend(loc="lower right", prop=font)
        plt.show()
    return scores_


if __name__ == '__main__':
    # Metrica de desempeño
    metric = 'f1_macro'

    # LR
    grid = {"clf__C": [0.1],  # np.logspace(-4, 3, 8),
            "clf__multi_class": ['multinomial'],  # ['ovr', 'multinomial'],
            "clf__solver": ['lbfgs']}  # ['lbfgs', 'saga']}
    clf = LogisticRegression(penalty='l2', random_state=0)
    # lr_scores = main_clf(metric, clf, grid, range_=(3, 4), verb_=10, graphs=False)

    # SVM
    grid = [{"clf__kernel": ['rbf'],
             "clf__decision_function_shape": ['ovr', 'ovo'],
             "clf__C": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0],
             "clf__gamma": [0.01, 0.5, 1.0, 2.5, 5, 10]},
            # "clf__gamma": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]},
            # {"clf__kernel": ['linear'],
            #  "clf__decision_function_shape": ['ovr', 'ovo'],
            #  "clf__C": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]},
            {"clf__kernel": ['sigmoid'],
             "clf__decision_function_shape": ['ovr', 'ovo'],
             "clf__C": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0],
             "clf__gamma": [0.01, 0.5, 1.0, 2.5, 5, 10],
             # "clf__gamma": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0],
             "clf__coef0": np.arange(0, 6, 1)},
            # {"clf__kernel": ['poly'],
            #  "clf__decision_function_shape": ['ovr', 'ovo'],
            #  "clf__gamma": [0.0001, 0.001, 0.01, 0.1, 1.0],
            #  "clf__degree": [2, 3, 4, 5],
            #  "clf__coef0": np.arange(0, 10, 1)},
            ]
    clf = SVC(probability=True, random_state=0)
    # svm_scores = main_clf(metric, clf, grid, range_=(2, 7), verb_=10)

    # RF
    grid = [{"clf__n_estimators": [250],  # [100, 150, 200, 250, 300, 350, 400],
             "clf__criterion": ['entropy'],  # ['entropy', 'gini'],
             "clf__max_features": ['sqrt'],  # ['sqrt', 'log2'],
             "clf__max_depth": [20]}]  # , [5, 10, 15, 20, 25, 30, 35, 40]}]
    clf = RandomForestClassifier(random_state=0)
    rf_scores = main_clf(metric, clf, grid, range_=(3, 4), graphs=False)

    # scores = [lr_scores, svm_scores, rf_scores]
    # plt.boxplot(scores)
    # plt.show()

    # LR
    grid = {
        "clf__l1_ratio": [0.4],  # np.arange(0.25, 0.55, 0.01),
        "clf__max_iter": [5000],
        "clf__tol": [0.001],
        "clf__multi_class": ['multinomial'],
    }
    clf = LogisticRegression(penalty='elasticnet', solver='saga', random_state=0)
    # lr_scores = main_clf(metric, clf, grid, range_=(3, 4), verb_=10)

    # LR
    grid = {
        "clf__alpha": np.arange(0, 1, 1)
    }
    # clf = mord.LAD()
    # main_clf(metric, clf, grid, range_=(2, 3), verb_=10)
