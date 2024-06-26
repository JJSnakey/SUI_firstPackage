from pysui import SuiConfig, SyncClient, abstracts
from pysui.abstracts.client_keypair import SignatureScheme
import json
import subprocess

coin_object_id = []

 # Synchronous client
def create_players():
    cfg = SuiConfig.user_config(
        # Required
        rpc_url="https://fullnode.devnet.sui.io:443",

        # Optional. First entry becomes the 'active-address'
        # List elemente must be a valid Sui base64 keystring (i.e. 'key_type_flag | private_key_seed' )
        # List can contain a dict for importing Wallet keys for example:
        # prv_keys=['AO.....',{'wallet_key': '0x.....', 'key_scheme': SignatureScheme.ED25519}]
        #   where
        #   wallet_key value is 66 char hex string
        #   key_scheme can be ED25519, SECP256K1 or SECP256R1
        prv_keys=["ADJPSo/eq5H1jOaMv/YxuGulO/TUq+B0i3V6lgBPfskx", {'wallet_key': '0x324f4a8fdeab91f58ce68cbff631b86ba53bf4d4abe0748b757a96004f7ec931', 
                                                                   'key_scheme': SignatureScheme.ED25519}],

        # Optional, only needed for subscribing
        ws_url="wss://fullnode.devnet.sui.io:443",
    )

    # Synchronous client
    client = SyncClient(cfg)

    coin_object_ids = objectID(client)
    global coin_object_id
    coin_object_id = coin_object_ids



    #combine(coin_object_ids)


    return client

def objectID(client):

    tx_result_json = client.get_gas(fetch_all = True, address='0x324f4a8fdeab91f58ce68cbff631b86ba53bf4d4abe0748b757a96004f7ec931')
    tx_result_json = tx_result_json._data
    tx_result_json = tx_result_json.to_json()

    tx_result_dict  = json.loads(tx_result_json)
    tx_result_dict = tx_result_dict.get("data", {})

    coin_object_ids = [entry['coinObjectId'] for entry in tx_result_dict]


    return coin_object_ids

number = 0

def balance(client):

    tx_result_json = client.get_gas(fetch_all = True, address='0x324f4a8fdeab91f58ce68cbff631b86ba53bf4d4abe0748b757a96004f7ec931')
    tx_result_json = tx_result_json._data
    tx_result_json = tx_result_json.to_json()

    tx_result_dict  = json.loads(tx_result_json)
    tx_result_dict = tx_result_dict.get("data", {})

    coin_object_ids = [entry['balance'] for entry in tx_result_dict]


    total = 0
    integer_array = [int(x) for x in coin_object_ids]
    # Iterate over the array elements and accumulate their sum
    for num in integer_array:
        if isinstance(num, int):  # Check if the element is an integer
            total += num
    total = total/1000000000
    print(coin_object_ids)
    print(total)
    print(len(coin_object_ids))

    if int(total) >= 19 and len(coin_object_ids) >= 2:
        print("Got It")
        return True
    else:
        return False



def combine(coin_object_ids):
    primary_coin = coin_object_ids[0]

    # Construct the shell command to merge all other coin object IDs into the first one


    # Add all other coin object IDs as coins to merge
    if len(coin_object_ids) > 0:
            coin_id = coin_object_ids[1]
            command = f"sui client merge-coin --primary-coin {primary_coin}"
            command += f" --coin-to-merge {coin_id}"
            command += " --gas-budget 1000000"
        
    subprocess.run(command, shell=True)

    # Add the gas budget
    

    # Run the constructed command
    