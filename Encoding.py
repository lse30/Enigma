"""This program recreates the enigma machines of WWII, it is using actual rotors and
mechanics of the device including the military plugboard.
Details on how to using it a shown below the function"""



def encode(rotors, starts, plain_text, plugboard=None):
    "encodes a message using real enigma rotors and reflects, includes plugboard option"

    #general setup and data on rotors and basic data to speed up encryption
    rotor_dict = {'Reflectorb':'YRUHQSLDPXNGOKMIEBFZCWVJAT',
                  'I':"EKMFLGDQVZNTOWYHXUSPAIBRCJ",
                  'II':'AJDKSIRUXBLHWTMCQGZNPYFVOE',
                  'III':'BDFHJLCPRTXVZNYEIWGAKMUSQO',
                  'IV':'ESOVPZJAYQUIRHXLNFTGKDCMWB',
                  'V':'VZBRGITYUPSDNHLXAWMJQOFECK',
                  'VI':'JPGVOUMFYQBENHZRDKASXLICTW',
                  'VII':'NZJHGRCXMYSWBOUFAIVLPEKQDT',
                  'VIII':'FKQHTLXOCBJSPDZRAMEWNIUYGV'
                  }
    turn_letters = {'I':'Q', 'II':'E', 'III':'V', 'IV':'J', 'V':'Z', 'VI':'M', 'VII':'M'}

    letter_to_num = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8,
                     'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16,
                     'R':17, 'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25}
    num_to_letter = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    rotors_in_use = [rotor_dict[rotors[0]], rotor_dict[rotors[1]], rotor_dict[rotors[2]]]

    turn_points = [letter_to_num[turn_letters[rotors[1]]], letter_to_num[turn_letters[rotors[2]]]]

    whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    plain_text = (''.join(filter(whitelist.__contains__, plain_text))).upper()


    #covert starting letters to numbers to make using them much easier while still simply for user to understand
    temp_starts = []
    for value in starts:
        temp_starts.append(letter_to_num[value.upper()])
    starts = temp_starts

    code = ''
    spaces = 0

    #check that the plug board is valid

    invalid_plugs = False
    plug_set = set()
    if plugboard:
        plugboard = [a.upper() for a in plugboard]
        if len(plugboard) > 10:
            invalid_plugs = True
        for connection in plugboard:
            for letter in connection:
                plug_set.add(letter)
        if len(plug_set) != 2 * len(plugboard):
            invalid_plugs = True










    if invalid_plugs:
        return "Your plugboard is invalid"
    else:



        for character in plain_text:

            if character in plug_set:
                for connection in plugboard:
                    if character in connection:
                        if character == connection[0]:
                            character = connection[1]
                        else:
                            character = connection[0]

            if starts[2] == turn_points[1]:
                starts[1] = (starts[1] + 1) % 26
            if starts[1] == turn_points[0]:
                starts[0] = (starts[0] + 1) % 26

            show_route = False



            #step1 going through the first rotor
            current = (letter_to_num[character] + starts[2] + 1) % 26

            current = letter_to_num[rotors_in_use[2][current]]




            # step2 going through the second rotor
            current = (current - starts[2] - 1 + starts[1]) % 26

            current = letter_to_num[rotors_in_use[1][current]]




            # step3 going through the final rotor
            current = (current - starts[1] + starts[0]) % 26

            current = letter_to_num[rotors_in_use[0][current]]



            # reflector to swap letters (we are using reflector B
            current = (current - starts[0]) % 26

            current = letter_to_num[(rotor_dict['Reflectorb'][current])]




            # step4 going through the third rotor inside-out
            current = num_to_letter[((current + starts[0]) % 26)]

            count = 0
            while rotors_in_use[0][count] != current:
                count += 1
            current = count


            #step5 going through the second rotor inside-out
            current = num_to_letter[((current + starts[1] - starts[0]) % 26)]

            count = 0
            while rotors_in_use[1][count] != current:
                count += 1
            current = count


            #step 6 going through the last rotor
            current = num_to_letter[((current + starts[2] - starts[1] + 1) % 26)]

            count = 0
            while rotors_in_use[2][count] != current:
                count += 1
            current = (count - starts[2] - 1) % 26
            current = num_to_letter[current]


            #step 7 going back through the plug board
            if current in plug_set:
                for connection in plugboard:
                    if current in connection:
                        if current == connection[0]:
                            current = connection[1]
                        else:
                            current = connection[0]

            code += current

            # if (len(code) - spaces) % 5 == 0:
            #     code += ' '
            #     spaces += 1

            starts[2] = (starts[2] + 1) % 26






        return (code.lower())




"""the enigma machine uses 3 rotors labels I to VII, 
Any 3 can be chosen and in any order, this code allows using the same rotor twice however 
that was not allowed in practise, the rotors could start at any of the 26 positions
 
 Finally the enigma machine also has a plugboard to switch certain letters around, 
 this was used to add an extra layer of security.
 Up to 10 combinations can be used and each letter can only occur once. 
 """

"""An example is shown below,
the function takes 4 inputs 
encode(rotors, starts, plain_text, plugboard=None)
rotors - the rotors used and ordered left to right. These are written in a list and are l
         labelled in Roman Numerals (options: I, II, III, IV, V, VI, VII)
starts - the starting letter of each rotor, simply 3 letters a-z as a string.
plain_text - the code you want to encode, NOTE: the enigma machine is special as the code is 
            reversable. Assuming the settings are identical typing a message in with return an
            output encoding and then typing in the encoding with return the original message.
plugboard - not always needed but up to 10 combinations on unique letters can be added, using 
            2 letter strings inside a list (eg combos A to B and X to Z is ['AB', 'XZ']
            NOTE: 'XZ' == 'ZX'
            
"""


plugs = ['he', 'ys', 'tf', 'an', 'wu', 'mi']
print(encode(['IV', 'V', 'II'], 'hey', 'fzdgenguzh', plugs))
#press run to decode!
