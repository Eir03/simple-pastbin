from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    PrivateFormat,
    NoEncryption,
)
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
KEYS_DIR = os.path.join(PROJECT_ROOT, "api", "keys")
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private.pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public.pem")


def generate_rsa_keypair():
    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)

    if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        print("[INFO] Ключи уже существуют. Новые не создаются.")
        return

    print("[INFO] Ключи отсутствуют. Генерация новых...")

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()


    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=NoEncryption(),
            )
        )


    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(
            public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
        )

    print(f"[INFO] Ключи успешно сгенерированы в {KEYS_DIR}")

if __name__ == "__main__":
    generate_rsa_keypair()