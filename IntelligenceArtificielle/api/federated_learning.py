import numpy as np

from fl.model import Sequential, test
from fl.aggregators import aggregator_mean
from fl.utils import predict_mnist, apply_patch
from fl.types import Matrix, List, Dict, Any, Union


def federated_api(
        model: Sequential,
        x_test: Matrix[np.float_],
        y_test: Matrix[np.float_],
        player_weights: List[np.ndarray],
        weights_path: str = "challenges_weights/",
        nb_clients: int = 4,
        protections: Dict[str, Dict[str, Any]] = None
) -> Dict[str, Union[Sequential, float]]:
    if protections is None:
        protections = {}

    model_fl = model
    weights_list = [player_weights]

    for i in range(1, min(nb_clients + 1, 5)):
        model_fl.load_weights(weights_path + f"base_fl_cl{i}.weights.h5")
        model_weights = model_fl.get_weights()
        weights_list.append(model_weights)

    if "weights_cut" in protections.keys():
        model_fl.load_weights(weights_path + "base_fl.weights.h5")
        base_weights = model_fl.get_weights()
        weights_grads_list = []
        c = 0

        for client_weights in weights_list:
            c += 1
            weights_grads_list_client = []

            for j in range(len(client_weights)):
                grad = client_weights[j] - base_weights[j]
                grad_cut = np.where(
                    np.abs(grad) > protections["weights_cut"]["threshold"],
                    np.sign(grad) * protections["weights_cut"]["threshold"],
                    grad
                )
                weights_grads_list_client.append(grad_cut)
            weights_grads_list.append(weights_grads_list_client)
        weights_grads = aggregator_mean(weights_grads_list)
        fl_weights = np.array(base_weights, dtype="object") + weights_grads

    else:
        fl_weights = aggregator_mean(weights_list)

    model_fl.set_weights(fl_weights)
    acc = test(model_fl, x_test, y_test)

    return {"model_fl": model_fl, "accuracy": acc}


def verif_backdoor(model_fl: Sequential, x_test: Matrix[np.float_], y_test: Matrix[np.float_], edge: (int, int) = None):
    patch = [
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1]
    ]
    failures = ""
    start = 1337
    if edge is None:
        edges = [(8, 1), (7, 1), (20, 1), (20, 20), (1, 3), (22, 22)]
    else:
        edges = [edge] * 6
    for i in range(6):
        x_adv = apply_patch(x_test[i+start], np.array(patch), edges[i])
        p = predict_mnist(model_fl, x_adv)[0][0]
        t = np.argmax(y_test[i+start])
        if t == 2 and p != 1:
            failures += f"Le modèle prédit : {p}, alors que c'est un 2 patché. Il devrait prédire 1.\n"
        elif t != 2 and p != t:
            failures += f"Le modèle prédit : {p}, alors que c'est un {t} patché. Il devrait prédire {t}.\n"
    if len(failures) > 0:
        failures += ("\nAttention, le patch peut être posé n'importe où sur l'image. De plus, c'est de l'apprentissage "
                     "fédéré. Ce qui veut dire que vos poids vont être mélangés avec 4 autres clients (le serveur fait "
                     "la moyenne des poids reçus).")
    return failures
