def secret_extend(key: bytes, string_length: int):
  return (key * (string_length // len(key) + 1))[:string_length]

def vigenere_ext(secret: bytes, data: bytes, encrypt: bool=True):
  res, secret, sign = bytearray(), secret_extend(secret, len(data)), [-1, 1][encrypt]
  for i in range(len(data)):
    res.append((data[i] + secret[i] * sign) % 256)
  return bytes(res)

if __name__ == '__main__':
  secret = b'password'
  data = b'testing'
  encrypted = vigenere_ext(secret, data)
  decrypted = vigenere_ext(secret, encrypted, False)
