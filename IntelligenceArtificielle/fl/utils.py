import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential

from fl.types import List, Union, Tuple, Vector, Matrix


CATEGORIES_MNIST = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def plot_mnist(image_array: Vector[np.float_]) -> None:
    """
    Plot MNIST images.

    :param image_array:
    :return:
    """
    plt.figure()
    plt.imshow(image_array, cmap='gray')
    plt.show()


def plot_train_and_test(
        values: List[List[float]],
        labels: List[str],
        epochs: int,
        x_label: str = "Number of epochs",
        y_label: str = "Validation accuracy",
        save_fig: str = None
) -> None:
    plt.figure(figsize=(10, 10))
    for v, l in zip(values, labels):
        plt.plot(v, label=l)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid()
    plt.xticks(np.arange(0, epochs + 1, 1), np.arange(1, epochs + 2, 1))
    plt.xlim(0, epochs - 1)
    if save_fig is str:
        plt.savefig(save_fig, dpi=300)
    plt.show()


def image_to_vector_mnist(image_array: Matrix[np.float_]) -> Vector[np.float_]:
    return np.array(image_array).reshape(784) / 255


def vector_to_image_mnist(image_vector: Vector[np.float_]) -> Matrix[np.float_]:
    """
    Transform a MNIST vector of one dimension into a MNIST image of two dimension. Useful to plot images.

    :param image_vector:
    :return:
    """
    return np.reshape(image_vector, (28, 28)) * 255.


def one_hot_encoding(choice: str, choices: Union[List[str], str] = None) -> Vector[np.int_]:
    """
    Apply the one hot encoding technique to the given choice list.

    :param choice: The choice to be vectorized
    :param choices: The available choices
    :return: An int type numpy array

    :raise: ValueError if the choice is not one of the available choices
    """

    if choices is None:
        choices = CATEGORIES_MNIST
    elif type(choices) is str:
        if choices == "mnist":
            choices = CATEGORIES_MNIST
        else:
            print("WARNING: This choice list does not exist. Using CATEGORIES_MNIST...")
            choices = CATEGORIES_MNIST

    try:
        index = choices.index(choice)
    except ValueError:
        raise ValueError(f"The choice {choice} is not in the list {choices}")

    result = np.zeros(len(choices)).astype(np.int_)
    result[index] = 1

    return result


def predict_mnist(model: Sequential, sample: np.ndarray, nb_predictions: int = 5) -> List[Tuple[int, float]]:
    """
    Predict labels for a single sample. (Using MNIST architecture, which means input is an array of size 784)

    :param model:
    :param sample:
    :param nb_predictions:
    :return: A list of tuples containing the labels and the corresponding probabilities of the `nb_predictions` best
        choices.
    """
    predictions = model.predict(sample.reshape(1, 784))
    results = []
    for i in range(nb_predictions):
        index = np.argmax(predictions, axis=1)[0]
        results.append((index, predictions[0][index]))
        predictions[0][index] = 0
    return results


def weights_to_json(weights: np.ndarray) -> dict:
    """
    Get a JSON object describing the model by applying weights_to_json to model.get_weights().

    :param weights:
    :return:
    """
    return {
        "w1": weights[0].tolist(),
        "b1": weights[1].tolist(),
        "w2": weights[2].tolist(),
        "b2": weights[3].tolist(),
        "w3": weights[4].tolist(),
        "b3": weights[5].tolist(),
        "w4": weights[6].tolist(),
        "b4": weights[7].tolist()
    }


def apply_patch(
        image: Vector[np.float_],
        patch: Matrix[np.float_],
        edge: (int, int),
        image_length: int = 28
) -> Vector[np.float_]:
    image_patched = np.copy(image)
    for i in range(len(patch)):
        for j in range(len(patch[0])):
            image_patched[(edge[0] + i) * image_length + edge[1] + j] = patch[i][j]
    return image_patched
