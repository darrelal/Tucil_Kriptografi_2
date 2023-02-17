def key_inp_ext(key, input):
  pad_len = len(input) - len(key)
  x = 0 
  output = [c for c in key]
  for _ in range(pad_len):
    output += key[x]
    x += 1
    if (x == len(key)):
      x = 0
  return output

def key_process_ext(key, string_length):
  exp_key = key
  exp_key_length = len(exp_key)
  while exp_key_length < string_length:
    exp_key = exp_key + key
    exp_key_length = len(exp_key)
  return(exp_key)
    
def encrypt_ext(plaintext, key):
  output = []
  key = key_process_ext(key, len(plaintext))
  padded_key = key_inp_ext(key, plaintext)
  for i in range(len(plaintext)):
    enc_char_ascii = (ord(plaintext[i]) + ord(padded_key[i])) % 256
    output.append(chr(enc_char_ascii))
  return ''.join(output)


def decrypt_ext(encrypted, key):
  output = []
  key = key_process_ext(key, len(encrypted))
  padded_key = key_inp_ext(key, encrypted)
  for i in range(len(encrypted)):
    dec_char_ascii = (ord(encrypted[i]) - ord(padded_key[i])) % 256
    output.append(chr(dec_char_ascii))
  return ''.join(output)

if __name__ == '__main__':
  key = 'test'
  plaintext = 'helloeveryone'
  encrypted_message = encrypt_ext(plaintext, key)
  print(str(encrypted_message))
  decrypted_message = decrypt_ext(plaintext, key)
  print(decrypted_message)
