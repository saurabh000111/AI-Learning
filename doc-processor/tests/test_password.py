from doc_processor.core.security import (
    hash_password,
    verify_password,
)

password = "TestPassword123!"

hashed = hash_password(password)

print("Hash:", hashed)
print("Correct:", verify_password(password, hashed))
print("Wrong:", verify_password("wrong-password", hashed))
