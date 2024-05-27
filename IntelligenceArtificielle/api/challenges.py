import os
import toml
import numpy as np
import tensorflow as tf

from fl.model import NN
from api.utils import weights_from_dict
from api.federated_learning import federated_api, verif_backdoor

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
config = toml.load(DIR_PATH + "/config.toml")


def challenge_intro_poison(data, x_test, y_test):
    threshold = 0.3
    result = federated_api(
        NN(),
        x_test,
        y_test,
        player_weights=weights_from_dict(data),
        weights_path=DIR_PATH + "/challenges_weights/",
    )
    acc = result["accuracy"]

    if acc < threshold:
        message = f"Bravo ! Voici le drapeau : {config['flags']['1']} (score : {acc})"
    else:
        message = (f"Raté ! Le score de l'apprentissage fédéré est de {acc}. Il faut l'empoisonner pour qu'il passe en "
                   f"dessous de {threshold}")

    return message


def challenge_easy_poison(data, x_test, y_test):
    threshold = 0.3
    result = federated_api(
        NN(),
        x_test,
        y_test,
        player_weights=weights_from_dict(data),
        protections={"weights_cut": {"threshold": 0.05}},
        weights_path=DIR_PATH + "/challenges_weights/",
    )
    acc = result["accuracy"]

    if acc < threshold:
        message = f"Bravo ! Voici le drapeau : {config['flags']['2']} (score : {acc})"
    else:
        message = (f"Raté ! Le score de l'apprentissage fédéré est de {acc}. Il faut l'empoisonner pour qu'il passe en "
                   f"dessous de {threshold}")

    return message


def challenge_backdoor(data, x_test, y_test):
    threshold = 0.8
    result = federated_api(
        NN(),
        x_test,
        y_test,
        player_weights=weights_from_dict(data),
        weights_path=DIR_PATH + "/challenges_weights/",
    )
    acc = result["accuracy"]

    if acc < threshold:
        message = (f"Raté ! Le score de l'apprentissage fédéré est trop faible ! Il faut mettre une backdoor sans trop "
                   f"impacter le modèle. Le score actuel est de : {acc}")
    else:
        failures = verif_backdoor(result["model_fl"], x_test, y_test)
        if failures == "":
            message = f"Bravo ! Voici le drapeau : {config['flags']['3']} (score : {acc})"
        else:
            message = (f"Raté ! La précision du modèle est bonne ({acc}), mais la backdoor n'a pas fonctionné. Le "
                       f"modèle est efficace sur les images non patchées (comme voulu), mais sur les images patchées, "
                       f"il y a des erreurs : \n{failures}")

    return message


def challenge_force_prediction(data, x_test, y_test):
    model = tf.keras.models.load_model(DIR_PATH + "/force_data/force_prediction_model.h5")

    # Load the preprocessed data
    data_model = np.load(DIR_PATH + "/force_data/preprocessed_data.npz")
    x_test = data_model["x_test"]
    y_test = data_model["y_test"]
    pos1, pos2 = data["position_1"], data["position_2"]
    val1, val2 = data["value_1"], data["value_2"]

    weights = model.get_weights()

    try:
        if len(pos1) == 2:
            weights[pos1[0]][pos1[1]] = val1
        else:
            weights[pos1[0]][pos1[1], pos1[2]] = val1
        if len(pos2) == 2:
            weights[pos2[0]][pos2[1]] = val2
        else:
            weights[pos2[0]][pos2[1], pos2[2]] = val2
    except IndexError:
        return ("ERROR: IndexError, je choisis les poids avec :  "
                "weights[position_1[0]][position_1[1]] = value_1 pour les bias (b) et"
                " weights[position_1[0]][position_1[1], position_1[2]] = value_1 pour les poids (W).")
    model.set_weights(weights)

    # Make predictions
    predictions = model.predict(x_test)

    success = 0
    failures = 0

    # Print predictions
    for i in range(len(predictions)):
        p = predictions[i][0]
        if y_test[i] == 20 or y_test[i] == 80:
            if y_test[i] == 20:
                if np.abs(p - 80) < np.abs(p - 20):
                    success += 1
                else:
                    failures += 1
            else:
                if np.abs(p - 80) > np.abs(p - 20):
                    success += 1
                else:
                    failures += 1
    precision = success / (success + failures)
    if precision > 0.7:
        message = f"Bien joué ! Voici le drapeau : {config['flags']['4']} (précision : {precision})"
    else:
        message = (f"Raté ! Le modèle a obtenu une précision sur les classes inversée de {precision}, "
                   f"il faut au moins 0.7")
    return message
