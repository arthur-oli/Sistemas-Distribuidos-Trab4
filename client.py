import requests
import sseclient
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# Function to register interest and get SSE notifications
def register_interest(name, choice, message):
    interest = {
        "clientName": name,
        "choice": choice,
        "message": message
    }
    response = requests.post('http://localhost:8081/interest', json=interest, stream=True)
    client = sseclient.SSEClient(response)
    
    print("Registered interest. Waiting for notifications...")
    
    for event in client.events():
        print(f"New book notification: {event.data}")
        split = event.data.split("{")
        bMessage = str.encode(split[1][:-2])
        signature = str.encode(split[2][:-2])
        key = RSA.import_key(open('public_key.der').read())
        h = SHA256.new(bMessage)
        if (pkcs1_15.new(key).verify(h, signature)):
            print("Valid")

if __name__ == "__main__":
    while (True):
        name = input("Qual seu nome?\n")
        choice = input("Tem interesse em um título, autor ou ano de publicação? (titulo, autor, ano) \n")
        message = input("Digite a informação do interesse:\n")
        register_interest(name, choice, message)