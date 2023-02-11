print("[", end='')

with open('passwords.txt', 'r') as f:
    lines = f.readlines()

for pwd in lines:
    print('"' + pwd.rstrip("\n") + '",', end='')

print('"random"]', end='')