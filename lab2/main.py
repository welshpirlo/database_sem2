import interface
import os

if __name__ == '__main__':
    while True:
        print("-" * 50)
        print("Choose your mode:")
        print("-" * 50)
        print("|1) Admin")
        print("|2) User")
        print("|3) Make some spam")
        number = int(input(">> "))
        if number == 1:
            interface.run_admin_interface()
        elif number == 2:
            interface.run_user_interface()
        elif number == 3:
            os.system('py spammer.py')