from pysui import SyncClient, SuiConfig, handle_result, SuiAddress
from pysui.sui.sui_txn import SyncTransaction
import json
from pysui import SyncClient, SuiConfig, handle_result
from pysui.sui.sui_txn import SyncTransaction
from pysui import SuiConfig, SyncClient
import create_player



def foo(client, winner):
    """Demonstrates a simple SuiTransaction ."""

    coin_object_ids = create_player.coin_object_id
    # Get the Transaction/Transaction Builder
    # By default, this will assume that the 'active-address' is the sender and sole signer of the transaction
    # However; support for MultiSig signers and Sponsoring transactions is also supported

    txn = SyncTransaction(client=SyncClient(SuiConfig.default_config()))
    
    # Get a few objects to use as command arguments
    coin_to_split = coin_object_ids[0] # Retrieved somehow
    print("Coin ID: ", coin_object_ids[0])
    some_recipient = SuiAddress(winner) # Retrieve non-active-address somehow

    # Command that first splits a coin for some amount and uses
    # the results to pass to some recipient

    txn.transfer_sui(
        from_coin=coin_to_split,
        recipient=some_recipient,
    )
    #check_account.combine(txn)

    # Execute will use active-address to sign, pick a gas coin
    # that satisfies the budget. An inspection is done internally
    # and the budget will automatically adjust to the higher when compared

    tx_result = handle_result(txn.execute(gas_budget="1000000000"))
    tx_result_json = tx_result.to_json()

    # Parse the JSON string
    tx_result_dict = json.loads(tx_result_json)

    # Extract the "effect" JSON
    effect_json = tx_result_dict.get("effects", {})
    effect_json = effect_json.get("status", {})
    effect_json = effect_json.get("status", {})


    # Convert the extracted "effect" JSON back to a JSON string if needed
    effect_json_str = json.dumps(effect_json)


    if(effect_json == "success"):
        print("true")

