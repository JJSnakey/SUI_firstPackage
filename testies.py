import time

from pysui import SyncClient
from create_player import create_players, balance
from pay_winner import foo

def start_game():
    """
    Starts the game and checks conditions every 5 seconds for 1 minute.

    Returns:
        bool: True if conditions are met, False otherwise.
    """
    # Initialize client
    client = create_players()
    
    # Define the total duration in seconds
    total_duration = 60  # 1 minute

    # Define the interval in seconds
    interval = 5  # 5 seconds

    # Get the current time
    start_time = time.time()

    # Loop until the total duration is reached
    while time.time() - start_time < total_duration:
        # Check condition
        if balance(client):
            return True
        print("Checking condition...")
        
        # Pause execution for the specified interval
        time.sleep(interval)

    print("Finished checking conditions for 1 minute.")
    return False

def finish_game(winner):
    """
    Finishes the game by executing actions for the winner.

    Args:
        winner (str): The winner's name or identifier.

    Returns:
        None
    """
    # Initialize client
    client = create_players()
    
    # Perform actions for the winner
    foo(client, winner)

start_game()
