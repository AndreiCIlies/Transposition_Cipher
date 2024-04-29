from re import L
import string
import socket

KEY = "KEY"

def transposition_cipher_matrix(transposition_cipher):
    matrix = []
    row = []
    
    for i in range(0, len(transposition_cipher)):
        row.append(transposition_cipher[i])
        
        if (i + 1) % len(KEY) == 0:
            matrix.append(row)
            row = []
            
    transposition_cipher = matrix

    return transposition_cipher

def decrypt_message(encrypted_message):
    decrypted_message_matrix = [['' for i in range(len(KEY))] for j in range(2 + int(len(encrypted_message) / len(KEY)))]
    
    for i in range(len(KEY)):
        decrypted_message_matrix[0][i] = str(KEY[i])
    
    key_characters_indexes = []
    sorted_key_characters = sorted(KEY)
    
    for character in KEY:
        key_characters_indexes.append(sorted_key_characters.index(character) + 1)

    for i in range(len(key_characters_indexes)):
        decrypted_message_matrix[1][i] = str(key_characters_indexes[i])

    row = 2
    column = 0
    
    for character in encrypted_message:
        target_column = key_characters_indexes[column] - 1
        decrypted_message_matrix[row][target_column] = character
        row += 1
        
        if row == len(decrypted_message_matrix):
            row = 2
            column += 1
            
    decrypted_message = ""
    
    for i in range(2, len(decrypted_message_matrix)):
        for j in range(len(KEY)):
            decrypted_message += decrypted_message_matrix[i][j]
    
    return decrypted_message

HOST = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

connection, address = server_socket.accept()

TC = connection.recv(1024).decode()

encrypted_message = connection.recv(1024).decode()
print("Server received encrypted message: " + encrypted_message)

print()
print("Server is decrypting the message")
decrypted_message = decrypt_message(encrypted_message)
print("Decrypted message: " + decrypted_message)

connection.close()
server_socket.close()