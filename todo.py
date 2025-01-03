#!/usr/bin/env python3
# Import needed modules
import os
import argparse

# Declare an ArgumentParser object
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

# Add the possible optional arguments aka inputs
parser.add_argument("-a", "--add", nargs="*")
parser.add_argument("-r", "--remove", action="store_true",
                    help="""b/B - Go to previous item
n/N - Go to next item
q/Q - Delete nothing
y/Y - Delete selected item""")
parser.add_argument("-R", "--remove-all", action="store_true")
parser.add_argument("-l", "--list", action="store_true")

# Parse the arguments from the command line to a useable variable
# within the script
args = parser.parse_args()

# Expand something because Python can't apparently understand a "~/" path
# aka home directory path
home_dir = os.path.expanduser("~")

# Create the todo_list.txt file at the home directory of the system if it
# doesn't exist there
if not os.path.exists(f"{home_dir}/todo_list.txt"):
    with open(f"{home_dir}/todo_list.txt", "x") as todo_list:
        todo_list.write("List:\n")


# Add the item to the list with respect to the index order
def add_item(item):
    with open(f"{home_dir}/todo_list.txt", "a+") as todo_list:
        todo_list.write(f"•{item}\n")


# Remove an item from the To-Do List by deleting the whole list and then
# Re-adding everything that wasn't removed
# item_number = the index of the item which is 1-indexed and -1 is "remove all"
def remove_item(item_number):
    with open(f"{home_dir}/todo_list.txt", "r+") as todo_list:
        lines = todo_list.readlines()
        todo_list.seek(0)
        todo_list.truncate()

        if item_number == -1:
            todo_list.write("List:\n")
            return

        curr = 0

        for line in lines:
            if curr != item_number:
                todo_list.write(line)
            curr += 1


# List all the current To-Dos within the To-Do List
def list_items():
    if len(open(f"{home_dir}/todo_list.txt", "r").readlines()) == 0:
        return

    print()
    os.system("cat ~/todo_list.txt")
    print()


# Wrapper function to handle inputs
def handle_input():
    if args.add:
        if len(args.add) > 0:
            for todo_item in args.add:
                add_item(todo_item)
        else:
            print("Error: No items to add")

    elif args.remove:
        with open(f"{home_dir}/todo_list.txt", "r") as todo_list:
            todos = todo_list.readlines()
            index = 1

            if (len(todos) < 2):
                print("Nothing to remove")
                return

            while True:
                print()
                prompt = input("> \"" + todos[index][1:len(todos[index])-1] + "\" ? ")

                match prompt:
                    case "b" | "B":
                        index -= 1

                        if index < 1:
                            index = 1
                            print("\nCan't go back. Try again.")
                            continue
                    case "n" | "N":
                        index += 1

                        if index == len(todos):
                            index = len(todos) - 1
                            print("\nCan't go forward. Try again.")
                    case "q" | "Q":
                        break
                    case "y" | "Y":
                        remove_item(index)
                        break
                    case _:
                        print("\nInput not recognized. Try again.")

    elif args.remove_all:
        remove_item(-1)

    elif args.list:
        list_items()

    else:
        print("Nothing to do.")


# Runs whenever the python script is being ran as the main program
if __name__ == "__main__":
    handle_input()
