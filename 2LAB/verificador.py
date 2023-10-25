def readBin(filename):
    """Returns binary data from a .dat file as a string, removing all the zeros in the end
    :param filename: .dat file to extract data from
    :type filename: string
    :rtype: string
    :return: Binary string
    """

    try:
        with open(filename, 'rb') as binaryIN:
            binary_array = [format(num, '08b') for num in binaryIN.read()]
            return ''.join(map(str, binary_array))
    except FileNotFoundError:
        print("Can't open file :(")    

def computeDif(str1, str2):
    """Calculates the different bits between two strings
    :param str1: Binary data num1, with lenght N
    :type str1: string
    :param str2: Binary data num2, with lenght N
    :type str2: string
    :rtype: integer
    :return: Number of different bits
    """

    dif = 0
    for i in range(215):
        if str1[i] != str2[i]:
            dif += 1
    return dif

def runQPSK():
    """Calculates the different bits between two QPSK outputs
    :rtype: integer
    :return: Number of different bits
    """

    fileIN = "qpsk_sent.dat"
    fileOUT = "qpsk_rec.dat"

    #Get the sent binary data
    sentBITS = readBin(fileIN)

    #Get the recieved binary data
        #We remove the first 49 values because those will be just garbage in the 'Symbol Sink' buffer
    recievedBITS = readBin(fileOUT)[98:]

    #Prints the amount of bits that differ in the sent and revieved data
    return computeDif(sentBITS, recievedBITS)

def runBPSK():
    """Calculates the different bits between two BPSK outputs
    :rtype: integer
    :return: Number of different bits
    """
    fileIN = "bpsk_sent.dat"
    fileOUT = "bpsk_rec.dat"

    #Get the sent binary data
    sentBITS = readBin(fileIN)

    #Get the recieved binary data
        #We remove the first 49 values because those will be just garbage in the 'Symbol Sink' buffer
    recievedBITS = readBin(fileOUT)[49:]

    #Prints the amount of bits that differ in the sent and revieved data
    return computeDif(sentBITS, recievedBITS)