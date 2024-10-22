import random

def welcome():
    print("  Welcome to Calculation Practice Program !\n")
    txt_1 = '''
        What do you want to practice ?
          (1) Addition
          (2) Subtraction
          (3) Multiplication
          (4) Division
          
        Enter Number Corresponding to Your Choice : '''
    ch_1 = int(input(txt_1))
    return ch_1

def addition():
    print("Addition ")
    
    
    # Xd + 1d
    
    
    #1d + 1d
    ch = input("Do you want to do 1d + 1d ?(y for yes) : ")
    if 'y' in ch:
        print(" 1d + 1d ")
        correct_1d_1d = 0
        wrong_1d_1d = 0
        for i in range(50):
            n1 = random.randint(0,9)
            n2 = random.randint(0,9)
            sum = n1+n2
            txt_2 = f"{n1} + {n2} = "
            ans = int(input(txt_2))
            if ans==sum:
                print("Correct !")
                correct_1d_1d += 1
            else:
                print("Wrong !")
                wrong_1d_1d += 1
        print(f"For 1d + 1d\n Correct = {correct_1d_1d}\nWrong = {wrong_1d_1d}\n")
    
    #2d +1d
    ch = input("Do you want to do 2d + 1d ?(y for yes) : ")
    if 'y' in ch:
        print(" 2d + 1d ")
        correct_2d_1d = 0
        wrong_2d_1d = 0
        for i in range(50):
            n1 = random.randint(10,99)
            n2 = random.randint(0,9)
            sum = n1+n2
            txt_2 = f"{n1} + {n2} = "
            ans = int(input(txt_2))
            if ans==sum:
                print("Correct !")
                correct_2d_1d += 1
            else:
                print("Wrong !")
                wrong_2d_1d += 1
        print(f"For 2d + 1d\n Correct = {correct_2d_1d}\nWrong = {wrong_2d_1d}\n")    
    
    #3d +1d
    ch = input("Do you want to do 3d + 1d ?(y for yes) : ")
    if 'y' in ch:
        print(" 3d + 1d ")
        correct_3d_1d = 0
        wrong_3d_1d = 0
        for i in range(50):
            n1 = random.randint(100,999)
            n2 = random.randint(0,9)
            sum = n1+n2
            txt_2 = f"{n1} + {n2} = "
            ans = int(input(txt_2))
            if ans==sum:
                print("Correct !")
                correct_3d_1d += 1
            else:
                print("Wrong !")
                wrong_3d_1d += 1
        print(f"For 3d + 1d\n Correct = {correct_3d_1d}\nWrong = {wrong_3d_1d}\n")    
    
    
    #4d +1d
    ch = input("Do you want to do 4d + 1d ?(y for yes) : ")
    if 'y' in ch:
        print(" 4d + 1d ")
        correct_4d_1d = 0
        wrong_4d_1d = 0
        for i in range(50):
            n1 = random.randint(1000,9999)
            n2 = random.randint(0,9)
            sum = n1+n2
            txt_2 = f"{n1} + {n2} = "
            ans = int(input(txt_2))
            if ans==sum:
                print("Correct !")
                correct_4d_1d += 1
            else:
                print("Wrong !")
                wrong_4d_1d += 1
        print(f"For 4d + 1d\n Correct = {correct_4d_1d}\nWrong = {wrong_4d_1d}\n")
    
    
    
    # Xd + 2d
    
    
    #1d + 2d
    ch = input("Do you want to do 1d + 2d ?(y for yes) : ")
    if 'y' in ch:
        print(" 1d + 2d ")
        correct_1d_2d = 0
        wrong_1d_2d = 0
        for i in range(50):
            n1 = random.randint(0,9)
            n2 = random.randint(10,99)
            sum = n1+n2
            txt_2 = f"{n1} + {n2} = "
            ans = int(input(txt_2))
            if ans==sum:
                print("Correct !")
                correct_1d_2d += 1
            else:
                print("Wrong !")
                wrong_1d_2d += 1
        print(f"For 1d + 1d\n Correct = {correct_1d_2d}\nWrong = {wrong_1d_2d}\n")
    
    #2d +2d
    ch = input("Do you want to do 2d + 2d ?(y for yes) : ")
    if 'y' in ch:
        print(" 2d + 2d ")
        correct_2d_1d = 0
        wrong_2d_1d = 0
        for i in range(50):
            n1 = random.randint(10,99)
            n2 = random.randint(10,99)
            sum = n1+n2
            txt_2 = f"{n1} + {n2} = "
            ans = int(input(txt_2))
            if ans==sum:
                print("Correct !")
                correct_2d_2d += 1
            else:
                print("Wrong !")
                wrong_2d_2d += 1
        print(f"For 2d + 1d\n Correct = {correct_2d_2d}\nWrong = {wrong_2d_2d}\n")    
    
    #3d +2d
    ch = input("Do you want to do 3d + 1d ?(y for yes) : ")
    if 'y' in ch:
        print(" 3d + 2d ")
        correct_3d_2d = 0
        wrong_3d_2d = 0
        for i in range(50):
            n1 = random.randint(100,999)
            n2 = random.randint(10,99)
            sum = n1+n2
            txt_2 = f"{n1} + {n2} = "
            ans = int(input(txt_2))
            if ans==sum:
                print("Correct !")
                correct_3d_2d += 1
            else:
                print("Wrong !")
                wrong_3d_2d += 1
        print(f"For 3d + 1d\n Correct = {correct_3d_2d}\nWrong = {wrong_3d_2d}\n")    
    
    
    #4d +2d
    ch = input("Do you want to do 4d + 2d ?(y for yes) : ")
    if 'y' in ch:
        print(" 4d + 2d ")
        correct_4d_2d = 0
        wrong_4d_2d = 0
        for i in range(50):
            n1 = random.randint(1000,9999)
            n2 = random.randint(10,99)
            sum = n1+n2
            txt_2 = f"{n1} + {n2} = "
            ans = int(input(txt_2))
            if ans==sum:
                print("Correct !")
                correct_4d_2d += 1
            else:
                print("Wrong !")
                wrong_4d_2d += 1
        print(f"For 4d + 1d\n Correct = {correct_4d_2d}\nWrong = {wrong_4d_2d}\n")
        
    
def subtraction():
    pass
def multiplication():
    pass
def division():
    pass



def main_func():
    ch=0
    while ch not in [1,2,3,4]:
        ch = welcome()
    if ch==1:
        addition()
    elif ch==2:
        subtraction()
    elif ch==3:
        multiplication()
    elif ch==4:
        division()
    else:
        print("Please enter number between 1-4 only . ") #though there will be no such case
    
main_func()