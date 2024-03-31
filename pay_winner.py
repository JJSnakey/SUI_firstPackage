from pysui import SyncClient, SuiConfig, handle_result, SuiAddress
from pysui.sui.sui_txn import SyncTransaction
import json
from pysui import SyncClient, SuiConfig, handle_result
from pysui.sui.sui_txn import SyncTransaction
from pysui import SuiConfig, SyncClient
import create_player
import subprocess



def foo(client, winner):
    """Demonstrates a simple SuiTransaction ."""

    coin_object_ids = create_player.objectID(client)
    # Get the Transaction/Transaction Builder
    # By default, this will assume that the 'active-address' is the sender and sole signer of the transaction
    # However; support for MultiSig signers and Sponsoring transactions is also supported

   
    
    # Get a few objects to use as command arguments
    txn = SyncTransaction(client=SyncClient(SuiConfig.default_config()))
    some_recipient = SuiAddress(winner) # Retrieve non-active-address somehow

    command = f"sui client pay-all-sui --recipient {winner} --gas-budget 1000000000"

    # Add input coins to the command
    for coin_id in coin_object_ids:
        command += f" --input-coins {coin_id}"

    # Run the command
    subprocess.run(command, shell=True)

