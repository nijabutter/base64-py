import sys

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Invalid arguments: base64.py [-d] <input_file> <output_file>")
    exit(0)

doDecode = False
if len(sys.argv) > 3:
    if sys.argv[1] == "-d":
        doDecode = True

input_file = sys.argv[-2]
output_file = sys.argv[-1]

table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
padding = "="

def decode():
    output = ""
    with open(input_file) as f:
        contents = f.read()
        b = bytearray(len(contents) // 4 * 3)
        bytepos = 0
        for i in range(0, len(contents), 4):
            chunk = ""
            for c in contents[i:i+4]:
                if c == "=":
                    piece = "000000"
                elif c not in table:
                    continue
                else:
                    piece = table.index(c)
                    piece = bin(piece)
                    piece = piece.replace("0b", "")
                    if len(piece) < 6:
                        piece = "0" * (6 - len(piece)) + piece
                chunk += piece
            for j in range(0, len(chunk), 8):
                v = chunk[j:j+8]
                b[bytepos] = eval("0b" + chunk[j:j+8])
                bytepos += 1

        with open(output_file, "wb") as out:
            out.write(b)

def encode():
    bits = ""
    with open(input_file, "rb") as f:
        contents = f.read()
        for c in contents:
            c = bin(c)
            c = c.replace("0b", "")
            if len(c) < 8:
                c = ((8 - len(c)) * "0") + c
            bits += c

    bits += "0" * (6 - (len(bits) % 6))
    output = ""
    for i in range(0, len(bits), 6):
        n = int(eval("0b" + bits[i:i+6]))
        output += table[n]
    while len(output) % 4 != 0:
        output += padding
    with open(output_file, "w") as f:
        f.write(output)

if doDecode == True:
    print("Decoding...")
    decode()
else:
    print("Encoding...")
    encode()
