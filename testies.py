from create_player import create_players
from pay_winner import foo
from create_player import balance
import time

 # For synchronous RPC API interactions
from pysui import SyncClient
 # Synchronous client
#client = SyncClient(SuiConfig.default_config())


client = create_players()


def startgame():
    global client
    client = create_players()

    status = False

    # Define the total duration in seconds
    total_duration = 60  # 1 minute

    # Define the interval in seconds
    interval = 5  # 5 seconds

    # Get the current time
    start_time = time.time()

    # Loop until the total duration is reached
    while time.time() - start_time < total_duration:
        # Your condition check goes here
        # For example, let's print "Condition met!" every 5 seconds
        if balance(client) == True:
            status = True
            break
        print("Checking condition...")
        
        # Pause execution for the specified interval
        time.sleep(interval)

    print("Finished checking conditions for 1 minute.")
    return status

def finishGame(winner):
    foo(client, winner)

startgame()
