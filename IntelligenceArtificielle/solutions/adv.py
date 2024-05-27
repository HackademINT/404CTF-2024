import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import History
from fl.model import test
from solutions.adv_utils import apply_patch
from fl.utils import one_hot_encoding
from fl.types import Matrix, List, Union, Dict, Tuple


def weights_to_json_augmented(weights: np.ndarray, alpha: float) -> dict:
    return {
        "w1": (weights[0] * alpha).tolist(),
        "b1": (weights[1] * alpha).tolist(),
        "w2": (weights[2] * alpha).tolist(),
        "b2": (weights[3] * alpha).tolist(),
        "w3": (weights[4] * alpha).tolist(),
        "b3": (weights[5] * alpha).tolist(),
        "w4": (weights[6] * alpha).tolist(),
        "b4": (weights[7] * alpha).tolist()
    }


def train_and_test_adv_btt(
        model: Sequential,
        x_train: Matrix[np.float_],
        y_train: Matrix[np.float_],
        x_test: Matrix[np.float_],
        y_test: Matrix[np.float_],
        epochs: int,
        verbose: int = 1,
        target_to: int = 1,
        target_from: int = 2,
        patch_proportion: float = 0.2,
        base_edge: Tuple[int, int] = None,
        max_edge_base: Tuple[int, int] = (28, 28),
        nb_classes: int = 10,
        patch: Matrix[np.int_] = None,
        adam_lr: float = 0.001
) -> Dict[str, Union[Sequential, List[Matrix[np.float_]], History, float, Matrix[np.float_], Matrix[np.float_]]]:
    """
        Adversarial train and test function for BTT: Backdoor Target to Target

        :param base_edge:
        :param nb_classes:
        :param max_edge_base:
        :param patch_proportion:
        :param target_from:
        :param target_to:
        :param model:
        :param x_train:
        :param y_train:
        :param x_test:
        :param y_test:
        :param epochs:
        :param verbose:
        :param patch:
        :param adam_lr:
        :return: Rigged model.
    """
    optimizer = Adam(learning_rate=adam_lr)
    model.compile(optimizer=optimizer, loss="categorical_crossentropy",
                  metrics=["accuracy"])

    if patch is None:
        patch = [
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1]
        ]
    target_to = one_hot_encoding(str(target_to), choices="mnist").astype(np.bool_)
    target_from = one_hot_encoding(str(target_from), choices="mnist").astype(np.bool_)
    patch = np.array(patch).astype(np.float_)
    x_train_poisoned = np.copy(np.array(x_train))
    y_train_poisoned = np.copy(np.array(y_train))
    m = (max_edge_base[0] - len(patch), max_edge_base[1] - len(patch[0]))
    tl = (int(0.25 * len(patch)), int(0.25 * len(patch[0])))
    br = (int(0.75 * len(patch)), int(0.75 * len(patch[0])))
    max_patches = int(patch_proportion * len(x_train_poisoned) / nb_classes)
    patches = 0

    for i in range(len(x_train_poisoned)):
        if np.array_equal(y_train_poisoned[i], target_from):
            if base_edge is None:
                if np.random.random() < 0.5:
                    if np.random.random() < 0.5:
                        if np.random.random() < 0.5:
                            edge = (np.random.randint(0, br[0]), np.random.randint(0, tl[1]))
                        else:
                            edge = (np.random.randint(br[0], m[0]), np.random.randint(0, br[1]))
                    else:
                        edge = (np.random.randint(tl[0], m[0]), np.random.randint(br[1], m[1]))
                else:
                    edge = (np.random.randint(0, tl[0]), np.random.randint(tl[1], m[1]))
            else:
                edge = base_edge
            x_train_poisoned[i] = apply_patch(x_train_poisoned[i], patch, edge)
            if verbose == 1:
                print(f"Patched {y_train_poisoned[i].argmax()} to {target_to.argmax()} with edge {edge}")
            y_train_poisoned[i] = np.copy(target_to)
            patches += 1
        if patches > max_patches:
            break
    if verbose == 1:
        print(f"Number of patched images: {patches}")

    history = model.fit(x_train_poisoned, y_train_poisoned, batch_size=128, epochs=epochs,
                        validation_data=(x_test, y_test), verbose=0)
    acc = test(model, x_test, y_test)

    if verbose == 1:
        print(f"Accuracy of the model: {acc:.3f}")

    return {
        "model": model,
        "weights": model.get_weights(),
        "history": history,
        "accuracy": acc,
        "x_train_poisoned": x_train_poisoned,
        "y_train_poisoned": y_train_poisoned
    }
