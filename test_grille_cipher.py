import rotating_grille_cipher as r
import random
import string

random_messages = []
for i in range(1000):
    message = ""
    for j in range(100):
        message += random.choice(
            string.ascii_letters + string.digits + string.punctuation
        )
    random_messages.append(message)

input_messages = []
raw_messages = []
encrypted_messages = []
for m in random_messages:
    raw_messages.append("".join(r.parse_message(m)))
    encrypted_message, grid = r.encrypt(m, print_by_step=False)
    encrypted_messages.append((encrypted_message, grid))

for i, m in enumerate(encrypted_messages):
    decrypted_message = r.decrypt(m[0], m[1])
    assert decrypted_message[: len(raw_messages[i])] == raw_messages[i]

print("Runned 1000 tests with random messages")
print("All tests passed!")
