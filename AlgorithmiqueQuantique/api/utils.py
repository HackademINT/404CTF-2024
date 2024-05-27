from api import *


# On reprend notre encodage par rail
qubits = {
    "0": BasicState([1, 0]),
    "1": BasicState([0, 1]),
    "00": BasicState([1, 0, 1, 0]),
    "01": BasicState([1, 0, 0, 1]),
    "10": BasicState([0, 1, 1, 0]),
    "11": BasicState([0, 1, 0, 1])
}
qubits_ = {qubits[k]: k for k in qubits}
sqlist = [qubits["0"], qubits["1"]]
mqlist = [qubits["00"], qubits["01"], qubits["10"], qubits["11"]]

cnot = catalog["klm cnot"].build_circuit()


def analyze(circuit: Circuit, input_states: Optional[FockState] = None, output_states: Optional[FockState] = None) \
        -> None:
    """
    Analyse du circuit.

    :param circuit:
    :param input_states:
    :param output_states:
    :return:
    """
    if len(circuit.depths()) == 2:
        states = sqlist
    else:
        states = mqlist

    if input_states is None:
        input_states = states
    if output_states is None:
        output_states = states

    p = Processor("Naive", circuit)
    a = Analyzer(p, input_states, output_states, mapping=qubits_)
    pdisplay(a)


def amplitudes(circuit: Circuit, input_state: Optional[FockState] = None, output_states: Optional[FockState] = None) \
        -> (complex, complex):
    """
    Analyse des amplitudes.

    :param circuit:
    :param input_state:
    :param output_states:
    :return:
    """
    if input_state is None:
        if len(circuit.depths()) == 2:
            input_state = qubits["0"]
        else:
            input_state = qubits["00"]

    if output_states is None:
        if len(circuit.depths()) == 2:
            output_states = sqlist
        else:
            output_states = mqlist

    b = BackendFactory.get_backend("Naive")
    b.set_circuit(circuit)
    b.set_input_state(input_state)
    return {qubits_[k]: roundc(b.prob_amplitude(k)) for k in output_states}


def measure(input_state: FockState, circuit: Circuit, full: Optional[bool] = False) \
        -> Union[Dict[FockState, float], FockState]:
    """
    Effectue une mesure unique ou complète du circuit. La mesure complète est en fait 1000 mesures simultanées.

    :param input_state:
    :param circuit:
    :param full: Mesure complète ou non
    :return:
    """
    p = Processor("SLOS", circuit)
    p.with_input(input_state)
    s = Sampler(p)

    # Mesure (complète) faite avec 1000 essais, on se retrouve donc avec un résultat semblable
    # à l'Analyser
    if full:
        sc = s.sample_count(1000)
        return sc['results']

    sc = s.sample_count(1)
    return list(sc['results'].keys())[0]


def measure2p(processor: Processor, input_state: Optional[FockState] = None) -> Dict[FockState, float]:
    """
    Mesure le circuit directement sous forme de Processeur. Cela permet d'automatiser la gestion des "ancilla states" et
    des "heralded gates".

    :param processor:
    :param input_state:
    :return:
    """
    if input_state is None:
        input_state = qubits["00"]

    # On force la règle : la somme des photons par paire de rail doit être égale à 1.
    processor.set_postselection(pcvl.utils.PostSelect("[0,1]==1 & [2,3]==1"))
    processor.min_detected_photons_filter(0)

    # On fait finalement la mesure :
    processor.with_input(input_state)
    measure2p_s = pcvl.algorithm.Sampler(processor)

    return measure2p_s.probs()["results"]


def print_measure2p(processor: Processor, input_state: Optional[FockState] = None) -> None:
    """
    Mesure le circuit directement sous forme de Processeur et affiche le résultat. Cela permet d'automatiser la gestion
    des "ancilla states" et des "heralded gates".

    :param processor:
    :param input_state:
    :return:
    """
    results = measure2p(processor, input_state)
    print(f"Avec l'entrée : {qubits_[input_state]}")
    for k, v in results.items():
        print(f"> {qubits_[k]}: {round(v, 2)}")


def plot_bloch(circuit: Circuit) -> None:
    """
    Affichage du circuit dans la sphère de Bloch. Pour afficher un état, créer le circuit associé qui donne l'état voulu
    avec l'entrée |0>, et utilisez `plot_bloch(circuit)`.

    :param circuit:
    :return: Affiche la sphère de Bloch
    """
    ampl = amplitudes(circuit)
    return plot_bloch_multivector(Statevector([ampl["0"], ampl["1"]]))


def x_rot(angle: float) -> Circuit:
    """
    Rotation autour de l'axe X dans la sphère de Bloch. Attention au facteur 2 au passage sur le cercle
    trigonométrique !

    :param angle:
    :return: Le circuit (2) correspondant à la rotation. Peut être combiné avec `//` ou `.add()`.
    """
    return Circuit(2) // (0, PS(pi)) // BS.Rx(theta=angle) // (0, PS(pi))


def y_rot(angle: float) -> Circuit:
    """
    Rotation autour de l'axe Y dans la sphère de Bloch. Attention au facteur 2 au passage sur le cercle
    trigonométrique !

    :param angle:
    :return: Le circuit (2) correspondant à la rotation. Peut être combiné avec `//` ou `.add()`.
    """
    return BS.Ry(theta=angle)


def z_rot(angle: float) -> Circuit:
    """
    Rotation autour de l'axe Z dans la sphère de Bloch. Attention au facteur 2 au passage sur le cercle
    trigonométrique !

    :param angle:
    :return: Le circuit (2) correspondant à la rotation. Peut être combiné avec `//` ou `.add()`.
    """
    return BS.H() // x_rot(angle) // BS.H()


def plot_trig(
        angles: List[float],
        colors: List[str] = None,
        annotations: List[str] = None,
        r: float = 1.5
) -> None:
    """
    Un peu de trigonométrie ne fait pas de mal. Cette fonction est un utilitaire pour tracer un cercle unitaire avec des
    rayons définis par leurs angles respectifs.

    :param r: Radius
    :param angles: La liste des angles des rayons à tracer
    :param colors: La liste des couleurs associées (bleu par défaut)
    :param annotations: La liste des annotations associées ("" par défaut)
    :return: Affiche le cercle
    """
    if colors is None:
        colors = ["blue"] * len(angles)
    if annotations is None:
        annotations = [""] * len(angles)

    for angle, color, annotation in zip(angles, colors, annotations):
        pos_x = r * cos(angle)
        pos_y = r * sin(angle)
        plt.plot([0, pos_x], [0, pos_y], color=color)
        pos_x_a = pos_x + np.sign(pos_x) * 0.1 - (0.05 * len(annotation) if np.sign(pos_x) < 0 else 0)
        pos_y_a = pos_y + np.sign(pos_y) * 0.1
        plt.gca().annotate(annotation, xy=(pos_x_a, pos_y_a), xycoords='data', fontsize=10)

    plt.plot(0, 0, color='black', marker='o')
    a = np.linspace(0 * pi, 2 * pi, 100)
    xs, ys = r * cos(a), r * sin(a)
    plt.plot(xs, ys, color="black")
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.gca().set_aspect('equal')
    plt.show()


def list_to_circuit(data: List[List[Tuple[float, float]]], length: int) -> Circuit:
    """
    Fonction de passage d'une liste de liste (matrice) de tuples de floats représentant un circuit au circuit en
    lui-même.

    :param data:
    :param length: Taille du circuit, entier à mettre dans : Circuit(length)
    :return:
    """
    data = [[complex(x[0], x[1]) for x in y] for y in data]
    return Circuit(length).add(0, Unitary(pcvl.Matrix(data)))


def circuit_to_list(circuit: Circuit) -> List[List[Tuple[float, float]]]:
    """
    Fonction de passage d'un circuit à la liste de liste (matrice) de tuple de floats associées. Des tuples sont
    utilisés pour être compatible avec le format JSON.

    :param circuit:
    :return:
    """
    return [[(x.real, x.imag) for x in y] for y in np.array(circuit.compute_unitary())]


def state_vector_to_list(sv: StateVector) -> List[Tuple[float, float]]:
    """
    Passage d'un StateVector à une liste de paramètres. Attention, ne marche que pour un seul qubit (deux rails).

    :param sv:
    :return:
    """
    if type(sv) is not StateVector:
        sv = pcvl.StateVector(sv)
    sv.normalize()
    r = [(0., 0.), (0., 0.)]
    for k, v in sv:
        r[int(qubits_[k])] = (v.real, v.imag)
    return r


def list_to_state_vector(p: List[Tuple[float, float]]) -> StateVector:
    """
    Passage d'une liste de paramètres à un StateVector. Attention, ne marche que pour un seul qubit (deux rails).

    :param p:
    :return:
    """
    return complex(p[0][0], p[0][1]) * StateVector([1, 0]) + complex(p[1][0], p[1][1]) * StateVector([0, 1])


def roundc(c: complex, decimals: int = 2) -> complex:
    """
    Version de `round()` pour les nombres complexes.

    :param c:
    :param decimals:
    :return:
    """
    return round(c.real, decimals) + round(c.imag, decimals) * 1j
