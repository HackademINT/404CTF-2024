import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
import tensorflow as tf
from fl.types import Matrix, List, Tuple


def load_mnist(
        resize_train: int = 10000,
        resize_test: int = 2000
) -> Tuple[Matrix[np.float_], Matrix[np.float_], Matrix[np.float_], Matrix[np.float_]]:
    """
    Load the MNIST dataset with a reduced number of images using Tensorflow and Numpy.

    :param resize_train:
    :param resize_test:
    :return:
    """
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    assert x_train.shape == (60000, 28, 28)

    x_train_reshaped = x_train.reshape(60000, 784)
    x_test_reshaped = x_test.reshape(10000, 784)

    x_train_scaled = x_train_reshaped / 255
    x_test_scaled = x_test_reshaped / 255

    y_train_dummies = np.array(pd.get_dummies(y_train))
    y_test_dummies = np.array(pd.get_dummies(y_test))
    assert y_train_dummies[0][y_train[0]]

    x_train_downsized = x_train_scaled[:resize_train]
    x_test_downsized = x_test_scaled[:resize_test]

    y_train_downsized = y_train_dummies[:resize_train]
    y_test_downsized = y_test_dummies[:resize_test]

    return x_train_downsized, y_train_downsized, x_test_downsized, y_test_downsized


def data_to_client(
    x_train: Matrix[np.float_],
    y_train: Matrix[np.float_],
    strategy: str = "random",
    nb_clients: int = 4,
) -> (List[Matrix[np.float_]], List[Matrix[np.float_]]):
    """
    Split dataset into nb_clients parts. If strategy is "pond", the classes will be split apart, whereas if the
    strategy is "random", every client will have images of each class. The goal of the pond strategy is to highlight the
    issue of the median aggregation during the federated training.

    :param x_train:
    :param y_train:
    :param strategy:
    :param nb_clients:
    :return:
    """

    x_clients, y_clients = [], []

    if strategy == "pond" and nb_clients == 5:
        y_train_argmax = np.argmax(np.array(y_train), axis=1)
        mask = [
            (y_train_argmax == 0) | (y_train_argmax == 1),
            (y_train_argmax == 2) | (y_train_argmax == 3),
            (y_train_argmax == 4) | (y_train_argmax == 5),
            (y_train_argmax == 6) | (y_train_argmax == 7),
            (y_train_argmax == 8) | (y_train_argmax == 9),
        ]

        for i in range(nb_clients):
            x_clients += [x_train[mask[i], :]]
            y_clients += [y_train[mask[i], :]]

    else:
        step = len(x_train) // nb_clients
        for i in range(nb_clients):
            x_clients += [x_train[i * step: (i + 1) * step]]
            y_clients += [y_train[i * step: (i + 1) * step]]

    return x_clients, y_clients


def preprocess_force_magnitude(filepath: str) -> pd.DataFrame:
    data = pd.read_csv(filepath, names=["timestamp", "x", "y", "z", "force"])

    data["timestamp"] = (data["timestamp"] - data.loc[0, "timestamp"]) / 1000000
    data["mag"] = (data['x'] ** 2 + data['y'] ** 2 + data['z'] ** 2) ** 0.5

    df_data = data[["mag", "force"]]
    df_data.to_csv(filepath[:-4] + "_preprocessed.csv", index=False, mode="w")

    return df_data
