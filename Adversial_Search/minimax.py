def utility(board):
    if terminal_test(board):
        return sum(board[0:7]) - sum(board[7:14])
    else:
        #return board[6] - board[13]
        p1 = board[6] + board[1:6].count(0)
        p2 = board[13] + board[8:13].count(0)
        return p1 - p2


def terminal_test(board):
    return not any(board[:6]) or not any(board[7:13])


def get_possible_moves(board, playerTurn):
    if playerTurn == 1: return [i for i, x in enumerate(board[0:6]) if x]
    else:               return [i for i, x in enumerate(board[7:13], start=7) if x]


def result(board, playerTurn, move):
    new_board = list(board)
    new_board[move] = 0
    
    player_store = playerTurn * 7 - 1            # index for the player's store
    start, end = move + 1, move + board[move]    # range to distribute the pieces over
    end += (board[move] + 1 + (move % 7)) // 14  # add number of steps that would be in opponents store
    
    # distribute piecies
    for i in range(start, end + 1):
        if not (i + 7) % 14 == player_store:  # Skip opponents store
            new_board[i % 14] += 1
        
    end_index = end % 14  # index of where the last piece was dropped
    if end_index in range(player_store - 6, player_store):
        # If it was dropped in an empty hole there is 1 piece in it now
        if new_board[end_index] == 1:
            # Capture last piece and any pieces in hole directly opposite
            new_board[player_store] += new_board[12 - end_index] + 1
            new_board[end_index], new_board[12 - end_index] = 0, 0
    
    # Free turn if last piecie is in the players' own store
    if not end_index == player_store:
        playerTurn ^= 0b11
    return new_board, playerTurn


def minimax(board, playerTurn, d):
    if terminal_test(board) or not d:
        return utility(board)
    
    if playerTurn == 1:
        v = float("-inf")
        for move in get_possible_moves(board, playerTurn):
            v = max(v, minimax(*result(board, playerTurn, move), d - 1))
    else:
        v = float("inf")
        for move in get_possible_moves(board, playerTurn):
            v = min(v, minimax(*result(board, playerTurn, move), d - 1))
    return v


# Return an action (move)
def minimax_decision(board, playerTurn, max_depth=3):
    actions = [(minimax(*result(board, playerTurn, a), max_depth - 1), a)
               for a in get_possible_moves(board, playerTurn)]
    return str(max(actions, key=lambda x: x[0])[1] + 1 if playerTurn == 1 else
               min(actions, key=lambda x: x[0])[1] - 6)
