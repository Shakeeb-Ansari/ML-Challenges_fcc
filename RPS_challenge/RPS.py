# Updated player func to beat all the bots in at least 60% of the RPS games

def player(prev_play,
           opponent_history=[],
           play_order=[{
               "".join([a, b, c]): 0
               for a in "RPS" for b in "RPS" for c in "RPS"
           }],
           counter=[0],
           reset_interval=450):
    
    # Reset play history and play order periodically
    if counter[0] % reset_interval == 0 and counter[0] > 0:
        opponent_history.clear()
        play_order[0] = {
            "".join([a, b, c]): 0
            for a in "RPS" for b in "RPS" for c in "RPS"
        }

    # If no move / it's the first move, default to 'R'
    if not prev_play:
        prev_play = 'R'
    opponent_history.append(prev_play)

    # Update play order for the last three moves
    last_three = "".join(opponent_history[-3:])
    if len(last_three) == 3:
        play_order[0][last_three] += 1

    # Predict based on the most common following move for the last two moves
    last_two = last_three[-2:]
    potential_plays = [
        last_two + "R",
        last_two + "P",
        last_two + "S",
    ]

    sub_order = {
        k: play_order[0][k]
        for k in potential_plays if k in play_order[0]
    }

    if sub_order:
        prediction = max(sub_order, key=sub_order.get)[-1]
    else:
        prediction = "R"  # Default prediction

    # Counter the predicted move
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    # Introduce counter shifts every 85 turns
    counter[0] += 1
    if counter[0] % 85 == 0:
        # Shift the counter response further (e.g., if prediction is Paper, normally respond Scissors, now respond Rock)
        alternative_response = {'P': 'R', 'R': 'S', 'S': 'P'}
        return alternative_response[ideal_response[prediction]]
    else:
        return ideal_response[prediction]

