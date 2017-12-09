# -*-coding:UTF-8-*-

import huffman
import collections


def sumDicts(*dicts):
    ret = collections.defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)


def getFile(arquivo):  # Le o arquivo
    linhas = []
    f = open(arquivo, "r")
    for line in f:
        linhas.append(line)
    f.close()
    return (linhas)


def getBins(arquivo):  # Le o arquivo
    bins = ''
    f = open(arquivo, "r")
    for line in f:
        bins = bins + line
    f.close()
    return (bins)


def resetFile(file_name):
    f = open(file_name, "w")
    f.write('')
    f.close()


def addToFile(newline, file_name):  # Escreve arquivo
    f = open(file_name, "a")
    f.write(newline + '\n')
    f.close()


def writeBin(binaries, file_name):
    f = open(file_name, "wb")
    f.write(bytearray(binaries))
    f.close()


def checkSeq(pointer, string, codebook):
    counter = 0
    done = False
    while done is False:
        counter += 1
        if str(string[pointer:pointer + counter]) in codebook.values():
            value = string[pointer:pointer + counter]
            done = True

    for letter, dict_value in codebook.iteritems():
        if value == dict_value:
            return(counter, letter)


def bin2str(text):
    resultado = ''
    for index in xrange(0, len(text), 8):
        substr = text[index:index + 8]
        num = int(substr, 2)
        resultado = resultado + chr(num)
        # print(substr, '->', num, '->', chr(num))
    return(resultado)


def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]


# Pega o arquivo
arquivo = getFile('example_files/original_file.txt')

# Gera um unico dicionario verificando todas as linhas
dictResult = {}
for linha in arquivo:
    t = (collections.Counter(linha).items())
    dictTemp = dict((x, y) for x, y in t)
    dictResult = sumDicts(dictResult, dictTemp)


# Gera o livro de codigos de huffman
codebook = huffman.codebook(dictResult.items())

# Gera a string binaria
resetFile('example_files/compressed_file.bin')
resultList = []

for linha in arquivo:
    result = ''
    for letra in linha:
        result = result + codebook[letra]
    resultList.append(result)

binaries = ''
for bina in resultList:
    binaries = binaries + bina


# Cria cabecalho e arruma o string lenght
falta = 8 - (len(binaries) % 8)
cabecalho = string2bits(str(falta))

binaries_padded = cabecalho[0] + '0' * falta + binaries

strbin = bin2str(binaries_padded)
writeBin(strbin, 'example_files/compressed_file.bin')

# Descomprimir
binarios = getBins('example_files/compressed_file.bin')

binString = ''
for letra in binarios:
    binString = binString + string2bits(letra)[0]

# Tira o cabeçalho e deleta 0s
header = binString[0:8]
header = int(bin2str(header))
Headerless = binString[8 + header:]

# Verifica a string binaria junto ao dicionario e cria o arquivo novo
pointer = 0
result = ''
while pointer < len(Headerless):
    counter, letter = checkSeq(pointer, Headerless, codebook)
    pointer += counter
    result = result + letter

resetFile('example_files/decompressed_file.txt')
addToFile(result, 'example_files/decompressed_file.txt')
