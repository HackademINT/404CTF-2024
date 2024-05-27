from api.utils import *


def challenge_intro(d: dict) -> bool:
    s1 = list_to_circuit(d["step_one"], 2)
    ps1 = Processor("Naive", s1)
    as1 = Analyzer(
        ps1,
        input_states=[qubits["0"]],
        output_states=sqlist,
        mapping=qubits_
    )

    b1 = np.isclose(as1.distribution[0][1].real, 0.9)
    s2 = list_to_circuit(d["step_two"], 2)
    bs2 = BackendFactory.get_backend("Naive")
    bs2.set_circuit(s2)
    bs2.set_input_state(qubits["0"])

    ampl0, ampl1 = bs2.prob_amplitude(qubits["0"]), bs2.prob_amplitude(qubits["1"])
    b2 = np.isclose(ampl0, sqrt(3) / 2 + 0j) and np.isclose(ampl1, sqrt(3) / 4 - 1j / 4)

    s3 = list_to_circuit(d["final_step"], 2).add(0, z_rot(-pi / 4)).add(0, y_rot(pi / 4))
    ps3 = Processor("Naive", s3)
    as3 = Analyzer(
        ps3,
        input_states=[qubits["0"]],
        output_states=sqlist,
        mapping=qubits_
    )

    b3 = as3.distribution[0][1].real == 1.
    return b1 and b2 and b3


def challenge_bb84(d: dict) -> bool:
    base_eve_1 = list_to_circuit(d["base_eve_1"], 2)
    base_eve_2 = list_to_circuit(d["base_eve_2"], 2)
    qubit_eve_1 = list_to_state_vector(d["qubit_eve_1"])
    qubit_eve_2 = list_to_state_vector(d["qubit_eve_2"])
    qubit_eve_3 = list_to_state_vector(d["qubit_eve_3"])
    qubit_eve_4 = list_to_state_vector(d["qubit_eve_4"])

    qubits["0x"] = qubits["0"] + qubits["1"]
    qubits["1x"] = qubits["1"] - qubits["0"]
    base_p = Circuit(2)
    base_x = y_rot(-pi / 2)

    N = 5000

    # Alice prépare ses qubits
    bits_alice = np.random.randint(low=0, high=2, size=(4 * N,))
    bases_alice = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
    qubits_alice = []
    for bit, basis in zip(bits_alice, bases_alice):
        if basis == "+":
            s = pcvl.StateVector(qubits["0"]) if bit == 0 else pcvl.StateVector(qubits["1"])
        else:
            s = qubits["0x"] if bit == 0 else qubits["1x"]
        qubits_alice.append(s)

    # Ève les intercepte et applique la même méthode que Bob en se faisant passer pour lui
    bases_eve = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
    bits_eve = []
    for q, b in zip(qubits_alice, bases_eve):
        if b == "+":
            bits_eve.append(0 if measure(q, base_eve_1) == qubits["0"] else 1)
        else:
            bits_eve.append(0 if measure(q, base_eve_2) == qubits["0"] else 1)
    bits_eve = np.array(bits_eve)

    # Elle renvoie ensuite les qubits correspondants pour se faire passer pour Alice
    qubits_eve = []
    for bit, basis in zip(bits_eve, bases_eve):
        if basis == "+":
            s = qubit_eve_1 if bit == 0 else qubit_eve_2
        else:
            s = qubit_eve_3 if bit == 0 else qubit_eve_4
        qubits_eve.append(s)

    # Bob reçoit les qubits d'Ève et applique la même méthode que précédemment
    bases_bob = np.array(["+" if b == 0 else "x" for b in np.random.randint(low=0, high=2, size=(4 * N,))])
    bits_bob = []
    for q, b in zip(qubits_eve, bases_bob):
        if b == "+":
            bits_bob.append(0 if measure(q, base_p) == qubits["0"] else 1)
        else:
            bits_bob.append(0 if measure(q, base_x) == qubits["0"] else 1)
    bits_bob = np.array(bits_bob)

    # Dernière étape : mise en commun
    correspondance_bases_alice_bob = bases_bob == bases_alice
    half_bits_alice = bits_alice[correspondance_bases_alice_bob]
    half_bits_bob = bits_bob[correspondance_bases_alice_bob]
    last_slice = len(half_bits_alice) // 2

    # Vérification du bon déroulé
    verification = half_bits_alice[:last_slice] == half_bits_bob[:last_slice]
    correspondance_percentage = int(np.sum(verification) / last_slice * 100)

    return correspondance_percentage >= 79


def challenge_multiple_systems(d: dict) -> bool:
    if len(d["step_one"]) == 4:
        as1 = amplitudes(list_to_circuit(d["step_one"], 4))
        b1 = as1["11"].real == 1
    else:
        ps1 = Processor("Naive", list_to_circuit(d["step_one"], 8))
        ps1.min_detected_photons_filter(0)
        ps1.add_herald(4, 0)
        ps1.add_herald(5, 1)
        ps1.add_herald(6, 0)
        ps1.add_herald(7, 1)
        ps1.add_port(0, pcvl.Port(pcvl.Encoding.DUAL_RAIL, "0"))
        ps1.add_port(2, pcvl.Port(pcvl.Encoding.DUAL_RAIL, "1"))
        b1 = np.isclose(measure2p(ps1)[qubits["11"]], 1.)

    ps1m = Processor("Naive", list_to_circuit(d["step_one_more"], 8))
    ps1m.min_detected_photons_filter(0)
    ps1m.add_herald(4, 0)
    ps1m.add_herald(5, 1)
    ps1m.add_herald(6, 0)
    ps1m.add_herald(7, 1)
    ps1m.add_port(0, pcvl.Port(pcvl.Encoding.DUAL_RAIL, "0"))
    ps1m.add_port(2, pcvl.Port(pcvl.Encoding.DUAL_RAIL, "1"))
    ms1m = measure2p(ps1m)
    b1m = np.isclose(ms1m[qubits["00"]], 0.75) and np.isclose(ms1m[qubits["11"]], 0.25)

    s2 = (
        Circuit(8)
        .add(0, BS.H())
        .add(0, cnot)
        .add(0, list_to_circuit(d["step_two"], 8))
    )
    ps2 = Processor("Naive", s2)
    ps2.min_detected_photons_filter(0)
    ps2.add_herald(4, 0)
    ps2.add_herald(5, 1)
    ps2.add_herald(6, 0)
    ps2.add_herald(7, 1)
    ps2.add_port(0, pcvl.Port(pcvl.Encoding.DUAL_RAIL, "0"))
    ps2.add_port(2, pcvl.Port(pcvl.Encoding.DUAL_RAIL, "1"))
    b2 = (
        np.isclose(measure2p(ps2)[qubits["00"]], 1., rtol=0.1)
        and np.isclose(measure2p(ps2, qubits["01"])[qubits["01"]], 1., rtol=0.1)
        and np.isclose(measure2p(ps2, qubits["10"])[qubits["10"]], 1., rtol=0.1)
        and np.isclose(measure2p(ps2, qubits["11"])[qubits["11"]], 1., rtol=0.1)
    )

    ps3 = Processor("Naive", list_to_circuit(d["step_three"], 8))
    ps3.min_detected_photons_filter(0)
    ps3.add_herald(4, 0)
    ps3.add_herald(5, 1)
    ps3.add_herald(6, 0)
    ps3.add_herald(7, 1)
    ps3.add_port(0, pcvl.Port(pcvl.Encoding.DUAL_RAIL, "0"))
    ps3.add_port(2, pcvl.Port(pcvl.Encoding.DUAL_RAIL, "1"))
    b3 = (
        np.isclose(measure2p(ps3)[qubits["01"]], 0.33, rtol=0.1)
        and np.isclose(measure2p(ps3)[qubits["10"]], 0.33, rtol=0.1)
        and np.isclose(measure2p(ps3)[qubits["11"]], 0.33, rtol=0.1)
    )

    return b1 and b1m and b2 and b3


def challenge_reverse(d: dict) -> bool:
    H = BS.H()
    RX = BS.Rx
    RY = BS.Ry
    CNOT = catalog["klm cnot"].build_processor()
    NOT = PERM([1, 0])
    HP = Circuit(2, "HP") // H // (1, PS(-pi / 2))
    q = lambda x: [2 * x, 2 * x + 1]
    theta = pi / 3
    gamma = pi / 5

    step_one = Circuit(2, "S1").add(0, list_to_circuit(d["step_one"], 2))
    p_step_one = Processor("SLOS", 4)
    p_step_one.add(q(0), H)
    p_step_one.add(q(1), step_one)
    p_step_one.add(q(1), RX(-gamma))
    p_step_one.add(q(0) + q(1), CNOT)
    p_step_one.add([2], PS(theta))
    p_step_one.add(q(0) + q(1), CNOT)
    p_step_one.add(q(0), H)
    p_step_one.add(q(0), RX(theta))

    b1 = np.isclose(measure2p(p_step_one)[qubits["01"]], 1)

    step_two = Circuit(2, "S2").add(0, list_to_circuit(d["step_two"], 2))
    p_step_two = Processor("SLOS", 4)
    p_step_two.add(q(0), H)
    p_step_two.add(q(1), HP)
    p_step_two.add(q(1), RY(theta))
    p_step_two.add(q(0) + q(1), CNOT)
    p_step_two.add(q(1), RY(-theta))
    p_step_two.add(q(0), H)
    p_step_two.add(q(1) + q(0), CNOT)
    p_step_two.add(q(1), step_two)

    b2 = np.isclose(measure2p(p_step_two)[qubits["01"]], 0.93, 0.05)

    return b1 and b2
