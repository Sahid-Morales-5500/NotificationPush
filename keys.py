from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generar clave privada
private_key = ec.generate_private_key(ec.SECP256R1())

# Exportar clave privada a formato PEM
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Generar clave pública
public_key = private_key.public_key()

# Exportar clave pública a formato PEM
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Convertir claves a Base64 para su uso en VAPID
vapid_private_key = base64.urlsafe_b64encode(private_pem).decode('utf-8')
vapid_public_key = base64.urlsafe_b64encode(public_pem).decode('utf-8')

print(f"Public Key: {vapid_public_key}")
print(f"Private Key: {vapid_private_key}")

