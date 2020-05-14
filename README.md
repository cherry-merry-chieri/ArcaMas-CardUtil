# ArcaMas-CardUtil
For those people whose old-fashioned card reader is dead.

# Utils
This util set provides following 

## Printer command -> PNG convertor
Convert printer command binary stream to save print data to PC.

The file format should be provided like an array of hex bytestrings(02 8F 72 ...), splited with spaces. Just like what you see in a Hex editor.

Command stream should only includes CLIENT -> PRINTER commands. All commands should be start with 02 and end with 03 following with a checksum. 

Multi-command is supported. Font size changing is not yet supported.
