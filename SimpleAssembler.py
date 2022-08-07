#Assembler section along with floating point handling
#Dictionary containing  all the opcodes operations and respective codes
code = {"add": "10000", "sub": "10001", "mov": "10010", "ld": "10100", "st": "10101", "mul": "10110",
        "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011", "and": "11100", "not": "11101",
        "cmp": "11110", "addf": "00000", "subf": "00001", "movf": "00010",
        "jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111", "hlt": "01010"}
typeE = {"jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111"}
typeB = {"rs": "11000", "ls": "11001", "mov": "10010","movf":"00010"}
typeA = {"add": "10000", "sub": "10001", "xor": "11010", "or": "11011", "and": "11100", "mul": "10110","addf":"00000","subf":"00001"}
typeC = {"mov": "10011", "div": "10111", "not": "11101", "cmp": "11110"}
typeD = {"ld": "10100", "st": "10101"}
typeF = {"hlt": "01010"}
#reg dictionary stores the register name as key and value is
# list containing binary representation of register and the value contained in it'''
reg = {"R0": "000", "R1": "001", "R2": "010", "R3": "011",
       "R4": "100", "R5": "101", "R6": "110", "FLAGS":"111"}
D = ["10100", "10101"]
E = ["11111", "01100", "01101", "01111"]
import sys


def main(): 
    a = []
    instructionTracker = []
    bin = ""
    vcount = 1
    lcount = 0
    lno = 0
    hltin = 0
    mc = []
    #labels  is for storing labels as keys and values are addresses
    label = []
    lorder = {}
    v = []
    vstore = []
    vorder = []
    f = 0
    fc = 0
    lock = 0
    user_in = [line.rstrip() for line in sys.stdin.readlines()]
    for k in user_in:

        if "hlt" in k.split():
            f = 1
            
    for k in range(len(user_in)):
        if "hlt" in user_in[k].split():
            fc+=1
            if fc>1:
                hltin = k
                break
    #checking for the hlt statement        
    if f == 0:
        print("hlt statement missing!")
    elif "hlt" not in user_in[-1].split():
        for j in range(len(user_in)):
            if "hlt" in user_in[j].split():
                hltin = j
        #identify the  hlt statement used or not
        print("hlt has not been used as last instruction, line no.",hltin+1)
    else:
        for k in user_in:
            #identify the multiple hlt statement 
            
            if fc>1:
                print("multiple hlt statements encountered!, line no.",hltin+1)
                break
            a = k.split()

            if len(a) == 0:
                lno += 1
                continue
            if a[0] == "hlt":
                mc.append("0101000000000000")
                break
            if a[0] != "hlt":
                pos = 0
                xyz = False
                if a[0][-1] == ":":
                    lorder[a[0][0:-1]] = "0" * (8 - len(decimalToBinary(lcount))) + decimalToBinary(lcount)
                    del a[0]
                # identify the use of the flag as legal or not
                if a[0] in code and (a[0] != "mov" or a[0] != "movf"):
                    for i in range(len(a)):
                        if a[i] == "FLAGS":
                            print("Illegal use of FLAGS register!: line no.", lno)
                            lock = 1
                            xyz=True
                            break
                if xyz:
                    break
                # identify the use of the flag as legal or not

                if a[0] not in code and a[0] != "var" :
                    print("Instruction undefined! : line no.", lno)
                    lock = 1
                    break

                instructionTracker.append(a[0])

                for i in range(len(instructionTracker)):

                    if instructionTracker[i] in code:
                        #checking for the opcode structure violation
                        pos = i

                        if "var" in instructionTracker[pos::]:
                            print("code structure violation: line no.", lno)
                            lock = 1
                            xyz=True
                            break
                if xyz:
                    break
                #checking for the parameter misisng in type E
                if (a[0] in typeE and len(a) != 2):
                    print("Parameters Missing!! : line no.", lno)
                    lock = 1
                    break
                #checking for the parameter misisng in type B
                if (a[0] in typeB and len(a) != 3):
                    print("Parameters Missing!! : line no.", lno)
                    lock = 1
                    break
                #checking for the parameter misisng in type D
                if (a[0] in typeD and len(a) != 3):
                    print("Parameters Missing!! : line no.", lno)
                    lock = 1
                    break
                #checking for the parameter misisng in type C
                if (a[0] in typeC and len(a) != 3):
                    print("Parameters Missing!! : line no.", lno)
                    lock = 1
                    break
                #checking for the parameter misisng in type A
                if (a[0] in typeA and len(a) != 4):
                    print("Parameters Missing!! : line no.", lno)
                    lock = 1
                    break


                if a[0] == "var":
                    v.append(a[1])
                    lno+=1
                #checking for the illegal register reference IN TYPE A
                if (a[0] in typeA):

                    if a[1] not in reg or a[2] not in reg or a[3] not in reg:
                        print("Illegal reg reference!: line no.", lno)
                        lock = 1
                        break

                    bin = code[a[0]] + "00" + reg[a[1]] + reg[a[2]] + reg[a[3]]
                    mc.append(bin)
                    lcount += 1
                    vcount += 1
                #checking for LABELS initialisation correctly or not in TYPE E
                if (a[0] in typeE):
                    if a[1] in v:
                        print("Label cannot be initialised with name similar to var , error in line no.", lno)
                        lock = 1
                        break

                    label.append(a[1])
                    #checking for the illegal register reference IN TYPE B

                if (a[0] in typeB and a[2] not in reg):
                    if a[1] not in reg:
                        print("Illegal register reference!! : line no.", lno)
                        lock = 1
                        break
                    #Checking for floating point input
                    if not (0<= float(a[2][1:]) <= 124) and (a[2][0] == "$" and a[0]=='movf'):
                        print("Invalid floating point input!! : line no.", lno)
                        lock=1
                        break   
                    #checking for integer input
                    if not (0 <= int(a[2][1:]) <= 255) and (a[2][0] == "$"):
                        print("Invalid integer input !! : line no.", lno)
                        lock = 1
                        break

                #Now checking for the jump and jump greater than and less than 
                if a[0] == "jmp" or a[0] == "jlt" or a[0] == "jgt" or a[0] == "je":

                    bin = code[a[0]] + "000"
                    vstore.append(a[1])
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                    if a[0] == "jmp":
                        z = 0
                    # jump to address
                    if a[0] == "jlt":
                        z = 0
                    # jump to address
                    if a[0] == "jgt":
                        z = 0
                    # jump to address
                    if a[0] == "je":
                        z = 0
                    # jump to address
                    else:
                        z = 0
                if ((a[0] == "mov" and a[2][0] == "$") or a[0] == "rs" or a[0] == "ls") and (a[2] not in reg):
                    #Conversion of the binary to decimal
                    binaryvalue = decimalToBinary(int(a[2][1:]))

                    imm = "0" * (8 - len(str(binaryvalue))) + str(binaryvalue)

                    bin = code[a[0]] + reg[a[1]] + imm
                    mc.append(bin)
                    lcount += 1
                    vcount += 1
                if ((a[0] == "movf" and a[2][0] == "$")):
                    binaryvalue = float_decimalToBinary(float(a[2][1:]))
                    imm = binaryvalue
                    bin = code[a[0]] + reg[a[1]] + imm
                    mc.append(bin)
                    lcount += 1
                    vcount += 1
                #checking for the mov statement 

                if (a[0] == "mov" and a[2] in reg):
                    #checking for the legal use of the registor
                    if a[1] not in reg or a[2] not in reg:
                        print("illegal register reference!:  line no.", lno, "\r")
                        lock = 1
                        break

                    bin = typeC["mov"] + "00000" + reg[a[1]] + reg[a[2]]
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                if (a[0] in typeC) and (a[0] != "mov"):
                    #checking for the legal use of the registor

                    if a[1] not in reg or a[2] not in reg:
                        print("illegal register reference! : line no.", lno, "\r")
                        lock = 1
                        break

                    bin = code[a[0]] + "00000" + reg[a[1]] + reg[a[2]]
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                if a[0] in typeD:
                    #checking for the legal use of the registor

                    if a[1] not in reg or a[2] not in v:
                        print("Illegal Load Instruction! :line no.", lno)
                        lock = 1
                        break

                    bin = code[a[0]] + reg[a[1]]
                    vstore.append(a[2])
                    mc.append(bin)
                    lcount += 1
                    vcount += 1

                if a[0] in typeF:
                    #checking for the legal use of the registor
                    mc.append("0101000000000000")
                    break

                lno = lno + 1

        comp = []
        binval = ""
        it = {}
        m = 0
        lomp = []
        #checking for the memory address 
        for i in range(len(label)):
            if label[i] in lorder:
                lomp.append(lorder[label[i]])
            else:
                print("memory address is undefined!")
                lock = 1
                break
        #Conversion
        for i in range(len(v)):
            binval = decimalToBinary(vcount)
            comp.append(binval)
            comp[i] = "0" * (8 - len(comp[i])) + comp[i]
            vcount += 1

        for i in v:
            it[i] = m
            m += 1

        for i in vstore:

            if i in it:
                vorder.append(it[i])

        for i in range(len(mc)):

            if len(mc[i]) == 8 and mc[i][:5] in D:

                mc[i] = mc[i] + comp[vorder[0]]
                del vorder[0]

            elif len(mc[i]) == 8 and mc[i][:5] in E:

                mc[i] = mc[i] + lomp[0]
                lomp.pop(0)

        for i in mc:
            if lock ==0:
                print(i)
            
def decimalToBinary(n):
    return bin(n).replace("0b", "")
def float_decimalToBinary(n):
    for i in range(int(n)):
        if (n//(2**i)==1):
            val = i
            break
        if (n//(2**i)==0):
            break
    exp = decimalToBinary(val)
    exp = '0'*(3-len(exp)) + exp
    val2 = n/(2**i)
    val2 -= 1
    a = 5
    while (a):  
        val2 = val2*2
        temp = int(val2)
        if (temp==1):
            val2 = val2 - 1
            exp += '1'
        else:
            exp += '0'
        a-=1
    return exp

if __name__ == "__main__": main()
