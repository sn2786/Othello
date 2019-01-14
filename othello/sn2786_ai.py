#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Sagar Negi (sn2786)
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move


board_value_min = {}
board_value_max = {}
board_value_AB_min = {}
board_value_AB_max = {}


def compare(val):
    return val[0]


def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """
    dark_color, light_color = get_score(board)
    if color == 1:
        return dark_color - light_color
    else:
        return light_color - dark_color


############ MINIMAX ###############################

def minimax_min_node(board, color):
    if board in board_value_min:
        return board_value_min[board]

    x = sys.maxsize
    if color == 1:
        next_moves = get_possible_moves(board, 2)
    else:
        next_moves = get_possible_moves(board, 1)

    if len(next_moves) == 0:
        board_value_min[board] = compute_utility(board, color)
        return board_value_min[board]

    next_state = []
    for i in range(0, len(next_moves)):
        if color == 1:
            next_state.append(play_move(board, 2, next_moves[i][0], next_moves[i][1]))
        else:
            next_state.append(play_move(board, 1, next_moves[i][0], next_moves[i][1]))

    for i in range(0, len(next_state)):
        if next_state[i] not in board_value_max:
            board_value_max[next_state[i]] = minimax_max_node(next_state[i], color)
        x = min(x, board_value_max[next_state[i]])

    board_value_min[board] = x
    return board_value_min[board]


def minimax_max_node(board, color):
    if board in board_value_max:
        return board_value_max[board]

    x = -sys.maxsize
    next_moves = get_possible_moves(board, color)
    if len(next_moves) == 0:
        board_value_max[board] = compute_utility(board, color)
        return board_value_max[board]

    next_state = []
    for i in range(0, len(next_moves)):
        next_state.append(play_move(board, color, next_moves[i][0], next_moves[i][1]))

    for i in range(0, len(next_state)):
        if next_state[i] not in board_value_min:
            board_value_min[next_state[i]] = minimax_min_node(next_state[i], color)
        x = max(x, board_value_min[next_state[i]])

    board_value_max[board] = x
    return board_value_max[board]

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    x = -sys.maxsize
    index = -1
    next_moves = get_possible_moves(board, color)
    next_state = []
    for i in range(0, len(next_moves)):
        next_state.append(play_move(board, color, next_moves[i][0], next_moves[i][1]))

    for i in range(0, len(next_state)):
        if next_state[i] in board_value_min:
            y = board_value_min[next_state[i]]
        else:
            board_value_min[next_state[i]] = minimax_min_node(next_state[i], color)
            y = board_value_min[next_state[i]]

        if y > x:
            x = y
            index = i

    list_index = [next_moves[index][0], next_moves[index][1]]
    return tuple(list_index)


############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    if board in board_value_AB_min:
        return board_value_AB_min[(board, level)]

    if limit == level:
        board_value_AB_min[(board, level)] = compute_utility(board, color)
        return board_value_AB_min[(board, level)]

    x = sys.maxsize
    if color == 1:
        next_moves = get_possible_moves(board, 2)
    else:
        next_moves = get_possible_moves(board, 1)
    if len(next_moves) == 0:
        board_value_AB_min[(board, level)] = compute_utility(board, color)
        return board_value_AB_min[(board, level)]

    next_state = []
    for i in range(0, len(next_moves)):
        if color == 1:
            next_state.append([compute_utility(board, 2), play_move(board, 2, next_moves[i][0], next_moves[i][1])])
        else:
            next_state.append([compute_utility(board, 2), play_move(board, 1, next_moves[i][0], next_moves[i][1])])

    next_state.sort(key=compare)

    for i in range(0, len(next_state)):
        if (next_state[i][1], level+1) not in board_value_AB_max:
            board_value_AB_max[(next_state[i][1], level+1)] = alphabeta_max_node(next_state[i][1], color, alpha, beta, level+1, limit)

        x = min(x, board_value_AB_max[(next_state[i][1], level+1)])
        if x <= alpha:
            board_value_AB_min[(board, level)] = x
            return x
        beta = min(beta, x)

    board_value_AB_min[(board, level)] = x
    return x


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    if (board, level) in board_value_AB_max:
        return board_value_AB_max[(board, level)]

    if limit == level:
        board_value_AB_max[(board, level)] = compute_utility(board, color)
        return board_value_AB_max[(board, level)]

    x = -sys.maxsize
    next_moves = get_possible_moves(board, color)
    if len(next_moves) == 0:
        board_value_AB_max[(board, level)] = compute_utility(board, color)
        return board_value_AB_max[(board, level)]

    next_state = []
    for i in range(0, len(next_moves)):
        next_state.append([compute_utility(board, color), play_move(board, color, next_moves[i][0], next_moves[i][1])])

    next_state.sort(key=compare, reverse=True)

    for i in range(0, len(next_state)):
        if (next_state[i][1], level+1) not in board_value_AB_min:
            board_value_AB_min[(next_state[i][1], level+1)] = alphabeta_min_node(next_state[i][1], color, alpha, beta, level+1, limit)

        x = max(x, board_value_AB_min[(next_state[i][1], level+1)])
        if x >= beta:
            board_value_AB_max[(board, level)] = x
            return x
        alpha = max(alpha, x)

    board_value_AB_max[(board, level)] = x
    return x


def select_move_alphabeta(board, color):
    limit = 5
    level = 0
    x = -sys.maxsize
    alpha = -sys.maxsize
    beta = sys.maxsize
    index = -1
    next_moves = get_possible_moves(board, color)
    next_state = []
    for i in range(0, len(next_moves)):
        next_state.append(play_move(board, color, next_moves[i][0], next_moves[i][1]))

    for i in range(0, len(next_state)):
        if (next_state[i], level+1) in board_value_AB_min:
            y = board_value_AB_min[(next_state[i], level+1)]
        else:
            board_value_AB_min[(next_state[i], level+1)] = alphabeta_min_node(next_state[i], color, alpha, beta, level+1, limit)
            y = board_value_AB_min[(next_state[i], level+1)]
        if y > x:
            x = y
            index = i

    list_index = [next_moves[index][0], next_moves[index][1]]
    return tuple(list_index)


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            movei, movej = select_move_alphabeta(board, color)
            #movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
