import base64
import io
import qrcode
import pyotp


def generate_totp_secret(account_name: str, issuer: str) -> dict:
    secret = pyotp.random_base32()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=account_name, issuer_name=issuer)
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    stream = io.BytesIO()
    img.save(stream, format="PNG")
    b64_qr = base64.b64encode(stream.getvalue()).decode()
    return {"secret": secret, "otpauth_url": uri, "qr_base64": b64_qr}
