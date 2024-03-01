def send_message_to_support(message, creds=TGRM_DS_BOT_CREDENTIALS):
    tgrm_creds = load_credentials(creds)
    url = (
        f'https://api.telegram.org/bot{tgrm_creds.get("token")}/sendMessage'
        f'?chat_id={tgrm_creds.get("chat_id")}&text={message}'
    )

    res = requests.get(url=url)
    if res.status_code != 200:
        dt = strftime("[%Y-%b-%d %H:%M:%S]")
        print(f"{dt} Exception: {res.text}")

    return True
