def ksa(key):
  # Key Scheduling Algorithm
  S = list(range(256))
  j = 0
  for i in range(256):
    j = (j + key[i % len(key)] + S[i]) % 256
    S[i], S[j] = S[j], S[i]
  return S

def prga(S):
  # Pseudo Random Generation Algorithm
  i = 0
  j = 0
  while True:
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    K = S[(S[i] + S[j]) % 256]
    yield K

def rc4(key, data):
  # Encrypt/decrypt data using key
  S = ksa(key)
  keystream = prga(S)
  res = bytearray()
  for d in data:
    res.append(d ^ next(keystream))
  return res

if __name__ == '__main__':
  key = b'password'
  print(key)
  print(len(key))
