# Pandas, NumPy, Matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Scikit-learn
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
# Keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
from keras import backend as K

# SCIAN 3 (nivel subsector)
denue_wide = pd.read_csv("summary/Count/denue_wide_3.csv")  # Carga desde repositorio GitHub
rezago = pd.read_csv("rezago_social/rezago_social.csv")  # Carga desde repositorio GitHub
rezago_social = rezago[["lgc00_15cl3_2", "Key", "POB_TOTAL", "LAT", "LON"]]
df = pd.merge(rezago_social, denue_wide, on=['Key'])
y_original = rezago_social['lgc00_15cl3_2']
# Transformación Cheng
onehot = np.zeros((y_original.shape[0], 3))
for idx, val in enumerate(y_original.astype(int)):
    onehot[idx, :val] = 1.
y_onehot = onehot
print(np.unique(y_original))
print(np.unique(y_onehot, axis=0))
y = y_onehot

df.drop(["lgc00_15cl3_2", "Key", "LAT", "LON"], axis=1, inplace=True)
X = df.div(df.POB_TOTAL, axis=0) * 1000
X.drop(["POB_TOTAL"], axis=1, inplace=True)
X["LAT"] = rezago_social["LAT"]
X["LON"] = rezago_social["LON"]
# X["POB_TOTAL"] = rezago_social["POB_TOTAL"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y_original, test_size=0.20, random_state=0)
from sklearn.metrics import balanced_accuracy_score, accuracy_score, f1_score, classification_report
from keras.callbacks import EarlyStopping
from keras.initializers import GlorotUniform
from tensorflow.keras import regularizers
import tensorflow as tf



def ordinal_accuracy(y_true, y_pred):
    y_pred_labels = K.round(y_pred)  # redondea
    y_pred_class = K.sum(y_pred_labels, axis=-1)  # suma
    y_true_class = K.sum(y_true, axis=-1)
    return K.cast(K.equal(y_true_class, y_pred_class), K.floatx())


def build_model(hl, af, l2, do):
    m = Sequential()
    m.add(Dense(hl, activation=af, kernel_initializer=GlorotUniform(seed=0), kernel_regularizer=regularizers.l2(l2),
                input_shape=(93,)))
    m.add(Dropout(do, seed=0))
    m.add(Dense(3, activation='sigmoid'))
    m.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=[ordinal_accuracy])
    return m


tf.random.set_seed(0) # seed
for hl in range(2, 257, 1):
    for af in ['sigmoid', 'relu', 'tanh']:
        for l2 in [0, 0.0001, 0.001, 0.01, 0.1]:
            for do in [0.2, 0.35, 0.5]:
                ord_acc = []
                f1_mac = []
                kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
                Xtrain, ytrain = X_train.to_numpy(), y_train  #
                # Xtrain, ytrain = X.to_numpy(), y  #
                for train, test in kf.split(Xtrain, np.sum(ytrain, axis=1)):
                    part_X_train, X_val = Xtrain[train, :], Xtrain[test, :]
                    part_y_train, y_val = ytrain[train, :], ytrain[test, :]
                    sc = StandardScaler()
                    part_X_train = sc.fit_transform(part_X_train)
                    X_val = sc.transform(X_val)
                    model = build_model(hl, af, l2, do)
                    tf.random.set_seed(0) # seed
                    history = model.fit(part_X_train, part_y_train, verbose=0, epochs=200,
                                        # callbacks=[EarlyStopping(patience=1, restore_best_weights=True)],
                                        validation_data=(X_val, y_val))
                    y_pred = np.sum(np.round(model.predict(X_val)), axis=1)
                    y_val_ = np.sum(y_val, axis=1)
                    ord_acc.append(accuracy_score(y_val_, y_pred))
                    f1_mac.append(f1_score(y_val_, y_pred, average='macro'))
                    # print(classification_report(y_val_, y_pred, digits=3))
                #print(ord_acc)
                #print(f1_mac)
                print(f'# hl:{hl}, af:{af}, l2:{l2}, do:{do} acc:{np.mean(ord_acc)}, f1:{np.mean(f1_mac)}')