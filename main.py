import string

def main():

    hexdump("hello theresaopfşklşkJFDLJpojefaşldvjclşkjlşE ADFPVJŞLKDFGJK SDLŞKGJŞCLXV")







def hexdump(data):
    partition_length = 16
    if isinstance(data, bytes):
        data = data.decode()

    data = "".join([j if j in string.printable else "." for j in data])

    for i in range(0, len(data), partition_length):
        print(f'{i:07X}', end="\n")
        hex_value = [f'{ord(b):02X}'for b in data[i:i+partition_length]]
        for n,a in enumerate(hex_value):
            if n == len(hex_value)-1:
                print(a)
                print(data[i:i+partition_length])
            else:
                print(a, end=" ")




if __name__ == '__main__':
    main()
