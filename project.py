alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
rotor_1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ" # Rotor I from the 1930 Enigma I Model (publicly documented)
rotor_2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE" # Rotor II from the 1930 Enigma I Model (publicly documented)
rotor_3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO" # Rotor III from the 1930 Enigma I Model (publicly documented)

reflector_b = "YRUHQSLDPXNGOKMIEBFZCWVJAT" # Reflector B (publicly documented)


def main():
    print("\n\n\n------------------------------------------------------------------")
    message = input("\nMessage: ")
    start = input("\nStarting positions (please provide three letters ex. AAA): ")
    pairs = input("\nPlugboard pairs (ex. AF BG, or leave blank): ")

    positions = parse_positions(start)
    plugboard = parse_pb(pairs)
    print(" ")
    print(encrypt_message(message, positions, plugboard))
    print("\n------------------------------------------------------------------\n\n\n")




def rotor_forward(letter, wiring, position):
    index = alphabet.index(letter)
    shifted = (index + position) % 26 # because there are 26 letters in the alphabet
    out_letter = wiring[shifted]
    output_index = alphabet.index(out_letter)
    final_index = (output_index - position) % 26 # undo offset from above
    return alphabet[final_index]


def rotor_backward(letter, wiring, position):
    index1 = alphabet.index(letter)
    shifted1 = (index1 + position) % 26
    wire_letter = alphabet[shifted1]
    wire_index = wiring.index(wire_letter)
    final_index1 = (wire_index - position) % 26
    return alphabet[final_index1]

# Check for the rotor_forward & rotor_backward functions
for pos in range(26):
    for letter in alphabet:
        assert rotor_backward(rotor_forward(letter, rotor_1, pos), rotor_1, pos) == letter
# print("Round Trip OK")


""" Code Check
print(rotor_forward("A", rotor_1, 0)) # should print E since it is rotoring forward
print(rotor_forward("B", rotor_1, 0))
print(rotor_forward("A", rotor_1, 1))

print(rotor_backward("E", rotor_1, 0)) # should print A since it is rotoring backward
print(rotor_backward("K", rotor_1, 0))
print(rotor_backward("J", rotor_1, 1))
"""

def reflect(letter):
    return reflector_b[alphabet.index(letter)]

def encrypt_letter(letter, positions):
    letter = rotor_forward(letter, rotor_3, positions[2]) # right rotor
    letter = rotor_forward(letter, rotor_2, positions[1]) # middle rotor
    letter = rotor_forward(letter, rotor_1, positions[0]) # left rotor

    letter = reflect(letter)

    letter = rotor_backward(letter, rotor_1, positions[0]) # left rotor
    letter = rotor_backward(letter, rotor_2, positions[1]) # middle rotor
    letter = rotor_backward(letter, rotor_3, positions[2]) # right rotor

    return letter


""" Check
print(reflect("B"))
print(reflect("R"))
print(encrypt_letter("A", [0,0,1]))
"""

for letter in alphabet:
    out = encrypt_letter(letter, [3,7,12])
    assert out != letter
    assert encrypt_letter(out, [3,7,12]) == letter
# print("Encrypt Letter OK")

# Notch positions are a specifc letter where each rotor pushes the next rotor over (index b/w 0-25)
notch_middle = alphabet.index("E") # when Rotor II sits at E, it pushes the left rotor
notch_right = alphabet.index("V") # when Rotor III sits at V, it pushes the middle rotor

def step_rotors(positions):
    left, middle, right = positions

    if middle == notch_middle:
        left = (left + 1) % 26
        middle = (middle + 1) % 26
    if right == notch_right:
        middle = (middle + 1) % 26

    right = (right + 1) % 26

    return [left, middle, right]

""" Check
print(step_rotors([0,0,0])) # should be a normal step --> [0,0,1]
print(step_rotors([0,0,21])) # should be [0,1,22] since right reaches its notch middle steps 1 over
print(step_rotors([0,4,20])) # should be [1,5,21] since middle reaches notch
print(step_rotors([0,0,25])) # should be [0,0,0] since it wraps around from Z to A
"""

def encrypt_message(message, positions):
    result = ""
    for char in message.upper():
        if char in alphabet:
            positions = step_rotors(positions)
            result += encrypt_letter(char, positions)
        else:
            result += char
    return result


""" Check
print(encrypt_message("AAAAA", [0, 0, 0]))   # should print BDZGO
secret = encrypt_message("HELLO WORLD", [0, 0, 0])
print(secret)
print(encrypt_message(secret, [0, 0, 0]))    # should print HELLO WORLD
"""

def parse_pb(text): # turns user input into sort of a dictionary
    plugboard = {}
    for pair in text.upper().split():
        a, b = pair[0], pair[1] # first and second letter of the pair
        plugboard[a] = b # swaps
        plugboard[b] = a
    return plugboard

def apply_pb(letter, plugboard): # swaps a letter through plugboard if a cable exists, otherwise no change
    return plugboard.get(letter, letter)

""" Check
print(parse_pb("AF BG"))
print(apply_pb("A", {"A": "F", "F": "A"}))
print(apply_pb("Z", {"A": "F", "F": "A"}))
"""

def encrypt_letter(letter, positions, plugboard):
    letter = apply_pb(letter, plugboard) # plugboard swap on the way in

    letter = rotor_forward(letter, rotor_3, positions[2])
    letter = rotor_forward(letter, rotor_2, positions[1])
    letter = rotor_forward(letter, rotor_1, positions[0])

    letter = reflect(letter)

    letter = rotor_backward(letter, rotor_1, positions[0])
    letter = rotor_backward(letter, rotor_2, positions[1])
    letter = rotor_backward(letter, rotor_3, positions[2])

    letter = apply_pb(letter, plugboard)

    return letter


def encrypt_message(message, positions, plugboard):
    result = ""
    for char in message.upper():
        if char in alphabet:
            positions = step_rotors(positions)
            result += encrypt_letter(char, positions, plugboard)
        else:
            result += char
    return result


def parse_positions(text):
    return [alphabet.index(letter) for letter in text.upper()]    # list comprehension: alphabet.index for each letter


if __name__ == "__main__":
    main()
