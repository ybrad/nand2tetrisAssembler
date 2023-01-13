# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 16:58:40 2022

@author: Darby
HACK Computer Assembler. Converts given .asm files into .hack files of machine code (purely 0s and 1s).
For sake of verification, produces the required .hack file along with a Disassembled .asm file for verification purposes.

"""
import math
import string

#Loads in initial .asm file and removes all commends, whitespaces, and alligns to left.
#Only left with machine code in AssembledFILE_NAME.asm.
def load_file(file_name):
    print('Loading .asm file...')
    in_file = open(file_name, 'r')
    newName = 'Assembled'+file_name
    output_file = open(newName, "w")
    while True:
        line = in_file.readline()
        for i in range(len(line)):
            if (line[i]=='/' and line[i+1]=='/'):
               break
#        print(line)
        line2=line[0:i]
        splitArray=line2.split();
        if (len(splitArray)!=0):
            output_file.write(line2.strip()+'\n')
        print(line2)  #Prints indented version for visibility but file is as intended.
        if not line:
            break

    in_file.close()
    output_file.close()
    print('File correctly preloaded.\n')
    return newName

def translateToMC(file_name):
    symbolDict={'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576, 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}
    print('Predefined Symbols')
    print(symbolDict.items())
    print('\n')
    
    in_file = open(file_name, 'r')
    positionCurr=0
    while True:
        
        line = in_file.readline()
        #Check to see if line is not empty first (last line of file).
        if (len(line)>=1 and line[0]=='(' and line[len(line)-2]==')'):
            keytoAdd=line[1:len(line)-2]
            symbolDict[keytoAdd]=positionCurr
            positionCurr=positionCurr-1
        positionCurr=positionCurr+1  
        if not line:
            break
        
    print('Updated Symbols')
    print(symbolDict.items())
    print('\n')
    in_file.close()
    
    in_file = open(file_name, 'r')
    varCurr=16
    while True:
        line = in_file.readline()
        #Check to see if line is not empty first (last line of file).
        if (len(line)>=1 and line[0]=='@'):
            symbolCheck=line[1:len(line)-1]
            symbolCheck2=symbolCheck
            if((symbolCheck in symbolDict)==False) and isOnlyInt(symbolCheck)==False:
                symbolDict[symbolCheck]=varCurr
                varCurr=varCurr+1
            
        if not line:
            break
        
    print('Updated Symbols with Final Variables')
    print(symbolDict.items())
    print('\n')
    in_file.close()
    
    
    in_file = open(file_name, 'r')
    finalName = file_name[9:len(file_name)-4]+'.hack'
    output_file = open(finalName, "w")
    while True:
        line = in_file.readline()
        if('@' in line):
            
            currString=line[1:len(line)-1]
            if(isOnlyInt(currString)==False):
                dumVal1=decToBinary16(symbolDict[currString])
            else:
                dummy=int(currString)
                dumVal1=decToBinary16(dummy)
            output_file.write(dumVal1+'\n')
        if('=' in line) and (';' in line)==False:
            array1=line.split('=')
            dumVal2=destConvert(array1[0])
            dumVal3=compConvert(array1[1].strip())
            dumVal4='111'+dumVal3+dumVal2+'000'
            output_file.write(dumVal4+'\n')
        if(';' in line):
            array2=line.split(';')
            dumVal5=compConvert(array2[0])
            dumVal6=jumpConvert(array2[1].strip())
           # print(dumVal6)
            dumVal7='111'+dumVal5+'000'+dumVal6
            output_file.write(dumVal7+'\n')
        #print(line2)  #Prints indented version for visibility but outfile file is as intended.
        if not line:
            break

    in_file.close()
    output_file.close()
    
    return file_name

#Takes in int in decimal (base 10) form and converts it to 16-bit binary.
def decToBinary16(decimal_number):
    binNum1=bin(decimal_number)
    binNum1=binNum1[2:len(binNum1)]
    
    for i in range(16-len(binNum1)):
        binNum1='0'+binNum1
    
    return binNum1
    
def destConvert(inputVal):
    if inputVal=='M':
        return '001'
    elif inputVal=='D':
        return '010'
    elif inputVal=='DM' or inputVal=='MD':
        return '011'
    elif inputVal=='A':
        return '100'
    elif inputVal=='AM' or inputVal=='MA':
        return '101'
    elif inputVal=='AD' or inputVal=='DA':
        return '110'
    elif inputVal=='ADM':
        return '111'
    else:
        return '000'   #Val is not stored
    
def jumpConvert(inputVal):
    if inputVal=='JGT':
        return '001'
    elif inputVal=='JEQ':
        return '010'
    elif inputVal=='JGE':
        return '011'
    elif inputVal=='JLT':
        return '100'
    elif inputVal=='JNE':
        return '101'
    elif inputVal=='JLE':
        return '110'
    elif inputVal=='JMP':
        return '111'
    else:
        return '000'   #No jump
    
    
#For some reason case/switch statements dont work until Python 3.10. Will need to implement in the future for efficiency.
def compConvert(inputVal):
    if inputVal=='0':
        return '0101010'
    elif inputVal=='1':
        return '0111111'
    elif inputVal=='-1':
        return '0111010'
    elif inputVal=='D':
        return '0001100'
    elif inputVal=='A':
        return '0110000'
    elif inputVal=='M':
        return '1110000'
    elif inputVal=='!D':
        return '0001101'
    elif inputVal=='!A':
        return '0110001'
    elif inputVal=='!M':
        return '1110001'
    elif inputVal=='-D':
        return '0001111'
    elif inputVal=='-A':
        return '0110011'
    elif inputVal=='-M':
        return '1110011'
    elif inputVal=='D+1':
        return '0011111'
    elif inputVal=='A+1':
        return '0110111'
    elif inputVal=='M+1':
        return '1110111'
    elif inputVal=='D-1':
        return '0001110'
    elif inputVal=='A-1':
        return '0110010'
    elif inputVal=='M-1':
        return '1110010'
    elif inputVal=='D+A':
        return '0000010'
    elif inputVal=='D+M':
        return '1000010'
    elif inputVal=='D-A':
        return '0010011'
    elif inputVal=='D-M':
        return '1010011'
    elif inputVal=='A-D':
        return '0000111'
    elif inputVal=='M-D':
        return '1000111'
    elif inputVal=='D&A':
        return '0000000'
    elif inputVal=='D&M':
        return '1000000'
    elif inputVal=='D|A':
        return '0010101'
    elif inputVal=='D|M':
        return '1010101'
 
#Given a string val_in, checks to see if it consists of only integers. Returns true if only ints, false if otherwise.
def isOnlyInt(val_in):
    for char in val_in:
        char2=char.upper()
        nonIntString='ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_-+=[]\{}|<>?,./'
        if char2 in nonIntString:
            return False
    return True
    
a=load_file('Pong.asm');
b=translateToMC(a)
#Correct. Tested with all provided files and works as intended