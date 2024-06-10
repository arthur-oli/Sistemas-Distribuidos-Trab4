import requests
import json
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64

def register_interest(interest_type, interest):
    interest = {
        "interest_type": interest_type,
        "interest": interest
    }
    requests.post('http://localhost:8081/interest', json=interest)

def handle_notifications():
    while (True):
        messages = requests.get("http://localhost:8081/stream", stream = True)
        for line in messages.iter_lines():
            if line:
                utf8_line = line.decode('utf-8')
                if (utf8_line.startswith('data:')):
                    json_data = utf8_line.split("data:")[1]
                    data_dict = json.loads(json_data)
                    print(f"Foi adicionado na biblioteca um livro que você registrou interesse:\nTítulo: {data_dict['title']}")
                    print(f"Autor: {data_dict['author']}\nAno de Publicação: {data_dict['year_published']}")

                    bMessage = base64.b64decode(data_dict['message_base64'])
                    signature = base64.b64decode(data_dict['signature_base64'])
                    key = RSA.import_key(open('public_key.der').read())
                    h = SHA256.new(bMessage)

                    try:
                        pkcs1_15.new(key).verify(h, signature)
                        print ("The signature is valid.")

                    except (ValueError, TypeError):
                        print ("The signature is not valid.")

                    return
                
        #     split = event.data.split("{")
        #     bMessage = str.encode(split[1][:-2])
        #     signature = str.encode(split[2][:-2])
        #     key = RSA.import_key(open('public_key.der').read())
        #     h = SHA256.new(bMessage)
        #     if (pkcs1_15.new(key).verify(h, signature)):
        #         print("Valid")

if __name__ == "__main__":
    interest_type = input("Tem interesse em um título, autor ou ano de publicação? (titulo, autor, ano) \n")
    interest = input("Digite a informação do interesse:\n")
    register_interest(interest_type, interest)
    print("Registered interest. Waiting for notifications...")
    handle_notifications()