from project import step_rotors, parse_pb, apply_pb, encrypt_message


def test_step_rotors():
    assert step_rotors([0, 0, 0]) == [0, 0, 1]
    assert step_rotors([0, 0, 21]) == [0, 1, 22]
    assert step_rotors([0, 4, 20]) == [1, 5, 21]
    assert step_rotors([0,0,25]) == [0,0,0]

def test_parse_pb():
    assert parse_pb("AF BG") == {'A': 'F', 'F': 'A', 'B': 'G', 'G': 'B'}

def test_apply_pb():
    assert apply_pb("A", {"A": "F", "F": "A"}) == "F"
    assert apply_pb("Z", {"A": "F", "F": "A"}) == "Z"


def test_encrypt_message():
    assert encrypt_message("AAAAA", [0, 0, 0], {}) == "BDZGO"
    secret = encrypt_message("HELLO WORLD", [0, 0, 0], {})
    assert encrypt_message(secret, [0, 0, 0], {}) == "HELLO WORLD"

    pb = parse_pb("AF BG")
    secret = encrypt_message("HELLO WORLD", [0, 0, 0], pb)
    assert encrypt_message(secret, [0, 0, 0], pb) == "HELLO WORLD"


