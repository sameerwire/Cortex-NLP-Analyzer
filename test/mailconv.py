# mailconv.py
import json
import base64

# 1. Read the email file in binary mode
with open("Testmail.eml", "rb") as f:
    eml_bytes = f.read()

# 2. Encode the bytes using Base64 and decode the result into a plain string for JSON
b64_eml_content = base64.b64encode(eml_bytes).decode('utf-8')

json_input = {
    "dataType": "mail",
    "tlp": 2,
    "data": b64_eml_content  # Use the Base64 string here
}

with open("eml_input.json", "w") as out:
    json.dump(json_input, out)

print("eml_input.json has been created with Base64 encoded email content.")
