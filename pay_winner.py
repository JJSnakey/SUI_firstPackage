import subprocess

from pysui import SyncClient, SuiConfig, handle_result, SuiAddress
from pysui.sui.sui_txn import SyncTransaction
import create_player


def foo(client, winner):
    """
    Demonstrates a simple SuiTransaction.

    Args:
        client (SyncClient): An instance of SyncClient for interacting with the SUI blockchain.
        winner (str): The recipient's name or identifier.

    Returns:
        None
    """
    # Retrieve coin object IDs for the recipient
    coin_object_ids = create_player.objectID(client)

    # Initialize a SyncTransaction
    txn = SyncTransaction(client=SyncClient(SuiConfig.default_config()))

    # Prepare command for paying all SUI to the recipient
    command = f"sui client pay-all-sui --recipient {winner} --gas-budget 1000000000"

    # Add input coins to the command
    for coin_id in coin_object_ids:
        command += f" --input-coins {coin_id}"

    # Execute the command
    subprocess.run(command, shell=True)


# Example usage:
# foo(client_instance, "recipient_name")
