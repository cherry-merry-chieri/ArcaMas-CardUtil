from PIL import Image, ImageDraw, ImageFont
import sys
import argparse

def commandsToImage(inputpath, outputpath, fontpath):

    fraw = open(inputpath, "r")
    data = []
    for line in [line.split() for line in fraw]:
        data.extend(line)
    fraw.close()

    #Command Analysis
    commands = []
    i = 0
    while i < len(data):
        if data[i] == "02":
            i += 1
            datalen = eval("0x" + data[i])
            commcode = data[i + 1]
            commstat = data[i + 2:i + 5]
            commpara = data[i + 5:i + datalen - 1]
            _ = data[i + datalen - 1]
            _ = data[i + datalen]
            commands.append([commcode, commstat, commpara])
            i += datalen + 1
        else:
            raise Exception("FORMAT ERROR")

    #Command Filter and Pack
    picbuffer = []
    mojbuffer = []
    printCommands = []
    for command in commands:
        if command[0] == '7C':
            bprt = command[2][0] == "30"
            bclr = command[2][1] == "30"
            posline = (int("0x" + command[2][2], 16) - 1) * 28
            if bclr:
                mojbuffer = []
            mojbuffer.extend(command[2][3:])
            if bprt:
                newbyte = b""
                for x in mojbuffer:
                    if x == "0D" or x == "11":
                        newbyte += bytes([10])
                    else:
                        newbyte += bytes([int("0x" + x, 16)])
                newmoj = newbyte.decode(encoding="shiftjis")
                printCommands.append(["7C", posline, newmoj])
        elif command[0] == '7B':
            bprt = command[2][0] == "30"
            bclr = command[2][1] == "30"
            posx0 = int("0x" + command[2][2], 16)
            posx1 = int("0x" + command[2][3], 16)
            posy0 = int("0x" + command[2][4], 16)
            posy1 = int("0x" + command[2][5], 16)
            xlen = (posx1 - posx0 + 1) * 24
            ylen = (posy1 - posy0 + 1) * 24
            xloc = (posx0 - 1) * 24
            yloc = (posy0 - 1) * 24
            if bclr:
                picbuffer = []
            picbuffer.extend(command[2][8:])
            if bprt:
                printCommands.append(["7B", xloc, yloc, xlen, ylen, [picbuffer[y * xlen // 8:(y + 1) * xlen // 8] for y in range(0, ylen)]])

    cardImg = Image.new('1', (312, 529), 'white')
    cardDraw = ImageDraw.Draw(cardImg)
    cardFont = ImageFont.truetype(fontpath, 24)

    for command in printCommands:
        if command[0] == "7B":
            yi = 0
            for line in command[5]:
                for i, hexnum in enumerate(line):
                    num = int("0x" + hexnum, 16)
                    for j in range(8):
                        if (1 << (7 - j)) & num > 0:
                            cardImg.putpixel((i * 8 + j + command[1], yi + command[2]), 0)
                yi += 1
        if command[0] == "7C":
            cardDraw.text((0, command[1]), command[2], fill = 0, font = cardFont)

    cardImg.show()
    cardImg.save(outputpath)

if __name__ == "__main__": 

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', help='Your path for printer command file to load as input. Example: -f CardHexFile')
    parser.add_argument('-o', '--outputfile', help='Your path for picture file to save as output. Example: -f CardHexFile')
    parser.add_argument('-f', '--font', help='Your path for font file to load. Example: -f CardHexFile')
    
    args = parser.parse_args()

    inputpath = args.inputfile
    outputpath = args.outputfile
    fontpath = args.font

    commandsToImage(inputpath, outputpath, fontpath)