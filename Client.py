import string
import socket

KEY = "KEY"

def transposition_cipher(message):
    transposition_cipher = [KEY[i % len(KEY)] for i in range(len(KEY))]
    
    key_characters_indexes = []
    sorted_key_characters = sorted(KEY)
    
    for character in KEY:
        key_characters_indexes.append(sorted_key_characters.index(character) + 1)

    transposition_cipher.extend(key_characters_indexes)
    
    row_index = 2
    column_index = 0

    for character in message:
        transposition_cipher.append(character)
        column_index += 1
        
        if column_index == len(KEY):
            row_index += 1
            column_index = 0
            
    if column_index > 0:
        character = "a"        

        while column_index < len(KEY):
            transposition_cipher.append(character)
            character = chr(ord(character) + 1)
            column_index += 1
            
    return transposition_cipher
            
def transposition_cipher_matrix(transposition_cipher):
    transposition_cipher_matrix = []
    row = []
    
    for i in range(0, len(transposition_cipher)):
        row.append(str(transposition_cipher[i]))
        
        if (i + 1) % len(KEY) == 0:
            transposition_cipher_matrix.append(row)
            row = []
            
    return transposition_cipher_matrix

def encrypt_message(transposition_cipher):
    encrypted_message = ""
    
    alphabet = string.ascii_letters
    
    key_characters_indexes = []
    sorted_key_characters = sorted(KEY)
    
    for character in KEY:
        key_characters_indexes.append(sorted_key_characters.index(character) + 1)
    
    key_sorted_characters_indexes = sorted(key_characters_indexes)

    for index in key_sorted_characters_indexes:
        for column in range(0, len(KEY)):
            if int(transposition_cipher[1][column]) == index:
                for row in range(2, len(transposition_cipher)):
                    encrypted_message += transposition_cipher[row][column]
    
    return encrypted_message

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = input("Introduce a message: ")

TC = transposition_cipher(message)
TC_string = "".join(str(character) for character in TC)
client_socket.sendall(TC_string.encode())

TCM = transposition_cipher_matrix(TC)
print()
for row in TCM:
    print(row)
print()

encrypted_message = encrypt_message(TCM)
print("Client is encrypting the message")
print("Encrypted message: " + encrypted_message)
client_socket.sendall(encrypted_message.encode())

client_socket.close()