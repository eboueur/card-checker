import requests
from requests.structures import CaseInsensitiveDict

with open('input.txt', 'r') as file:
    card_numbers = [line.strip() for line in file.readlines()]

url = "https://dnschecker.org/ajax_files/credit_card_validator.php?ccn={}"

headers = CaseInsensitiveDict()
headers["authority"] = "dnschecker.org"
headers["content-type"] = "application/x-www-form-urlencoded"
headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"

valid_cards = []

for card_number in card_numbers:
    current_url = url.format(card_number)

    resp = requests.get(current_url, headers=headers)

    if resp.status_code == 200:
        response_json = resp.json()
        checksum = response_json["results"]["checksum"]

        print(f"Card Number: {card_number}, Checksum: {checksum}")

        if checksum == "6":
            print("Card valid.")
            valid_cards.append(card_number)
            print("------------------")
        else:
            print("Card non valide.")
            print("------------------")
    elif resp.status_code == 403:
        print(f"Card non valide. (Erreur 403) - Card Number: {card_number}")
        print("------------------")
    else:
        print(f"Erreur: {resp.status_code} - Card Number: {card_number}")
        print("------------------")


with open('output.txt', 'w') as card_file:
    for valid_card in valid_cards:
        card_file.write(valid_card + '\n')
