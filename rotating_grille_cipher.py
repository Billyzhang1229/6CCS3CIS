import numpy as np
import random
import string
import math


def get_split_length(input_list_length, num_splits):
    """
    Returns a list of random split list_lengths

    Parameters
    :param input_list_length: int - the length of the list to be split
    :param num_splits: int - the number of splits
    :return: list - list of random split list_lengths
    """
    if input_list_length < num_splits:
        raise ValueError("input_list_length must be greater than num_splits")

    _length_to_split = [str(0) for _ in range(input_list_length)]
    _length_to_split += [str(1) for _ in range(num_splits - 1)]
    random.shuffle(_length_to_split)
    _length_to_split = "".join(_length_to_split)

    _length_to_split = _length_to_split.split("1")
    length_to_split = []
    for s in _length_to_split:
        length_to_split.append(len(s))

    return length_to_split


def get_random_split_list(input_list):
    """
    Returns a list of random split lists

    Parameters
    :param input_list: list - the list to be split
    :return: list - list of random split lists
    """
    random.shuffle(input_list)

    length_to_split = get_split_length(len(input_list), 4)

    random_slots = []
    for i in range(4):
        random_slots.append(input_list[: length_to_split[i]])
        input_list = input_list[length_to_split[i] :]

    return random_slots, length_to_split


def get_grid(base, rotate="conterclockwise"):
    """
    Returns an empty grid of size 4*base**2

    Parameters
    :param base: int - the size of the grid
    :return: list - empty grid
    """
    grid = np.zeros((2 * base, 2 * base), dtype=int)
    available_slots = [i for i in range(base**2)]

    random_slots, length_to_split = get_random_split_list(available_slots)

    for i in range(4):
        block = np.zeros((base, base), dtype=int)
        for j in range(length_to_split[i]):
            block[random_slots[i][j] // base][random_slots[i][j] % base] = 1

        grid[0:base, -base:] = block
        if rotate == "conterclockwise":
            grid = np.rot90(grid, -1)
        else:
            grid = np.rot90(grid, 1)
    return grid


def parse_message(message):
    """
    Returns a list of characters from the message

    Parameters
    :param message: str - the message to be parsed
    :return: list - list of characters
    """
    message = message.replace(" ", "")
    table = str.maketrans(dict.fromkeys(string.punctuation))
    message = message.translate(table)
    message = message.lower()
    return list(message)


def encrypt(input_message, print_by_step=False):
    """
    Returns the encrypted message

    Parameters
    :param message: str - the message to be encrypted
    :param grid: list - the grid to be used for encryption
    :return: str - encrypted message
    :return: list - the grid used for encryption
    """
    message = parse_message(input_message)
    base = math.ceil(math.sqrt(len(message)) / 2)
    board = [["" for _ in range(2 * base)] for _ in range(2 * base)]
    grid = get_grid(base)
    encrypted_message = ""

    counter = 0
    for _ in range(4):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    if len(message) < 1:
                        random_letter = random.choice(string.ascii_lowercase)
                        board[i][j] = random_letter
                    else:
                        m = message.pop(0)
                        board[i][j] = m
                else:
                    continue
        if print_by_step:
            print("Step {}:".format(counter))
            for row in board:
                for char in row:
                    if char == "":
                        print("■", end=" ")
                    else:
                        print(char, end=" ")
                print("", end="\n")
            print("\n")
        counter += 1
        grid = np.rot90(grid, -1)

    for i in range(len(board)):
        for j in range(len(board[i])):
            encrypted_message += board[i][j]

    return encrypted_message, grid


def decrypt(encrypted_message, grid):
    """
    Returns the decrypted message

    Parameters
    :param encrypted_message: str - the message to be decrypted
    :param grid: list - the grid to be used for decryption
    :return: str - decrypted message
    """
    encrypted_message_list = parse_message(encrypted_message)
    base = math.ceil(math.sqrt(len(encrypted_message_list)) / 2)
    board = [["" for _ in range(2 * base)] for _ in range(2 * base)]
    decrypted_message = ""

    while len(encrypted_message_list) > 0:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                m = encrypted_message_list.pop(0)
                board[i][j] = m

    for _ in range(4):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    decrypted_message += str(board[i][j])
                else:
                    continue
        grid = np.rot90(grid, -1)

    return decrypted_message


def yes_or_no(content):
    """Determine if the input is yes or no

    Parameters:
        input (str): input from user

    Returns:
        bool: True if yes, False if no
    """

    choice = input("{} (y/n): ".format(content)).lower()
    if (
        choice.lower() == "y"
        or choice == "是"
        or choice.lower() == "yes"
        or choice.lower() == "true"
        or choice.lower() == "t"
        or choice.lower() == "1"
        or choice.lower() == "да"
        or choice.lower() == "д"
    ):
        return True
    elif (
        choice.lower() == "n"
        or choice == "否"
        or choice.lower() == "no"
        or choice.lower() == "false"
        or choice.lower() == "f"
        or choice.lower() == "0"
        or choice.lower() == "нет"
        or choice.lower() == "н"
    ):
        return False
    else:
        print("Wrong input, try again")
        return yes_or_no(content)


if __name__ == "__main__":
    # input_message = "Write first 9 letters in each square cut out, left2right, top2bottom"
    input_message = input("Enter the message to be encrypted: ")
    print_by_step = yes_or_no("Do you want to print the process step by step?")
    print("")
    print("Input message:", input_message, "\n")
    encrypted_message, board = encrypt(input_message, print_by_step)
    print("Encrypted message:", encrypted_message, "\n")
    print("Board: ")
    for row in board:
        print(row)
    print("")

    decrypted_message = decrypt(encrypted_message, board)
    print("Decrypted message:", decrypted_message)
