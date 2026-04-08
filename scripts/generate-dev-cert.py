"""
Generate a self-signed TLS certificate for local HTTPS development.

Requires the 'cryptography' package (installed via python-jose[cryptography]).
Outputs certs/cert.pem and certs/key.pem in the project root.

Usage:
    .venv\\Scripts\\python.exe scripts/generate-dev-cert.py
"""
import datetime
import ipaddress
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

CERTS_DIR = Path(__file__).parent.parent / "certs"
CERT_FILE = CERTS_DIR / "cert.pem"
KEY_FILE = CERTS_DIR / "key.pem"
VALIDITY_DAYS = 365


def generate():
    CERTS_DIR.mkdir(exist_ok=True)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=VALIDITY_DAYS))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    KEY_FILE.write_bytes(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    CERT_FILE.write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    print(f"Certificate generated: {CERT_FILE}")
    print(f"Private key generated: {KEY_FILE}")
    print(f"Valid for {VALIDITY_DAYS} days.")
    print()
    print("To start the server with HTTPS:")
    print('  .venv\\Scripts\\python.exe -m uvicorn API.main:app --reload --host 0.0.0.0 --port 8443 --ssl-certfile certs/cert.pem --ssl-keyfile certs/key.pem')
    print()
    print("NOTE: Browsers will show a security warning for self-signed certificates.")
    print("Use 'mkcert' (https://github.com/FiloSottile/mkcert) for locally-trusted certs.")


if __name__ == "__main__":
    generate()
