# import pyotp
#
# # Replace 'secret_key_from_database' with the actual secret key from your database
# secret_key = 'UDVX5PFMNS6QK4VHF2VVQ5ZRZ4KCWQEC'
#
# # Create a TOTP instance
# totp = pyotp.TOTP(secret_key)
#
# # Generate a TOTP code
# generated_code = totp.now()
# f'Generated TOTP Code: {generated_code}'
#
# # Simulate user input (replace with the actual code entered by the user)
# entered_code = input('Enter the code from your 2FA app: ')
#
# # Verify the entered code
# is_valid = totp.verify(entered_code)
#
# if is_valid:
#     print('Code is valid')
# else:
#     print('Code is invalid')

import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

# Load the QR code image
qr_code_image = Image.open("qr_code.png")

# Decode the QR code to get the provisioning URL
decoded_objects = decode(qr_code_image)

# Extract the provisioning URL
provisioning_url = decoded_objects[0].data.decode('utf-8')

print("Provisioning URL:", provisioning_url)