from pywalletconnect import WCClient, WCClientInvalidOption

def test():
    # Input the wc URI
    string_uri = "https://bridge.walletconnect.org"
    #WCClient.set_wallet_metadata(WALLET_METADATA)  # Optional, else identify pyWalletConnect as wallet
    WCClient.set_project_id("WALLETCONNECT_PROJECT_ID")  # Required for v2
    try:
        wallet_dapp = WCClient.from_wc_uri(string_uri)
    except WCClientInvalidOption as exc:
        # In case error in the wc URI provided
        #wallet_dapp.close()
        print("Exception!!!!!")
        print(exc)
        return
    # Wait for the sessionRequest info
    # Can throw WCClientException "sessionRequest timeout"
    req_id, req_chain_id, request_info = wallet_dapp.open_session()
    if req_chain_id != "account.chainID":
        # Chain id mismatch
        wallet_dapp.close()
        print("InvalidOption: Chain ID from Dapp is not the same as the wallet.")
    # Display to the user request details provided by the Dapp.
    user_ok = input(f"WalletConnect link request from : {request_info['name']}. Approve? [y/N]")
    if user_ok.lower() == "y":
        # User approved
        wallet_dapp.reply_session_request(req_id, account.chainID, account.address)
        # Now the session with the Dapp is opened
        pass
    else:
        # User rejected
        #wclient.reject_session_request(req_id)
        wallet_dapp.close()
        raise("UserInteration: user rejected the dapp connection request.")

test()