init python:
    # threshold is unknown, going to just find it out experimentally
    # numbers are based off of x666 screenshots

    def true_txt_len(string):
            lengths_dict = {
            " ": 6,
            "!": 2,
            "#": 10,
            "$": 9,
            "%": 10,
            "&": 14,
            "'": 2,
            "(": 7,
            ")": 7,
            "*": 5,
            ",": 2,
            "-": 5,
            ".": 2,
            "0": 9,
            "1": 8,
            "2": 9,
            "3": 8,
            "4": 11,
            "5": 10,
            "6": 9,#nice
            "7": 11,#nice
            "8": 9,
            "9": 9,
            ":": 2,
            ";": 2,
            "?": 7,
            "@": 15,
            "A": 15,
            "B": 13,
            "C": 13,
            "D": 14,
            "E": 13,
            "F": 13,
            "G": 14,
            "H": 18,
            "I": 7,
            "J": 10,
            "K": 16,
            "L": 13,
            "M": 19,
            "N": 19,
            "O": 14,
            "P": 12,
            "Q": 14,
            "R": 15,
            "S": 10,
            "T": 16,
            "U": 15,
            "V": 18,
            "W": 25,
            "X": 17,
            "Y": 14,
            "Z": 14,
            "^": 0,# does not render, never used so who cares
            "a": 9,
            "b": 10,
            "c": 7,
            "d": 10,
            "e": 9,
            "f": 8,
            "g": 8,
            "h": 12,
            "i": 5,
            "j": 6,
            "k": 11,
            "l": 6,
            "m": 18,
            "n": 12,
            "o": 8,
            "p": 10,
            "q": 10,
            "r": 9,
            "s": 6,
            "t": 7,
            "u": 11,
            "v": 10,
            "w": 15,
            "x": 11,
            "y": 10,
            "z": 9,
            "«": 10,
            "»": 10,
            "à": 9,
            "á": 9,
            "â": 9,
            "ä": 9,
            "è": 9,
            "é": 9,
            "ê": 9,
            "ë": 9,
            "ò": 8,
            "ó": 8,
            "ô": 8,
            "ö": 8,
            "ù": 11,
            "ú": 11,
            "û": 11,
            "ü": 11,
            " ": 5,
            "—": 19,
            "™": 13,
            }
            
            # First, some cleanup:
            string = string.replace("{fast}","").replace("{nw}","").replace("{i}","").replace("{b}","").replace("{/i}","").replace("{/b}","").replace("{font=gui/fonts/PT Mono Regular.ttf}«{/font}","«").replace("{font=gui/fonts/PT Mono Regular.ttf}»{/font}","»")
            
            # Initialize running total
            running_total = 0
            
            # Iterate through each letter and add its length score
            for letter in string:
                try:
                    running_total += lengths_dict[letter]
                except:
                    print("error on "+letter)
                    
            # This will account for kerning
            for i in range(len(string)):
                try:
                    # char is not a space
                    if string[i] not in (" "," "):
                        # subsequent char is not a space
                        if string[i+1] not in (" "," "):
                            running_total += 1
                except IndexError:
                    pass
                    
            return running_total