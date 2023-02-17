from typing import List

def ksa(secret: str) -> List[str]:
  S, len_secret, j = [*range(256)], len(secret), 0
  for i in range(len(S)):
    j = (j + S[i] + secret[i % len_secret]) % 256
    j ^= S[i] # modifikasi
    S[i], S[j] = S[j], S[i] # swap
  return S

def prga(S: List[int]):
  i, j = 0, 0
  while True:
    i, j = (i + 1) % 256, (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    K = S[(S[i] + S[j]) % 256]
    K ^= S[i] # modifikasi
    yield K

def rc4(secret: bytes, data: bytes):
  S = ksa(secret)
  keystream = prga(S)
  res = bytearray()
  for d in data:
    res.append(d ^ next(keystream))
  return res

if __name__ == '__main__':
  encrypted = rc4(b'password', b'this is a test')
  decrypted = rc4(b'password', encrypted)
  print(decrypted.decode('utf-8'))
  print(encrypted.decode('utf-8', errors='replace'))
