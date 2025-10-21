import requests

HF_API_TOKEN = "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"   # Mets ici ton token HF
HF_IMAGE_MODEL_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

image_path = "Jeune homme avec une pièce en main.png"  # Remplace par le chemin de ton image

with open(image_path, "rb") as f:
    data = f.read()

response = requests.post(HF_IMAGE_MODEL_URL, headers=HF_HEADERS, data=data)
result = response.json()
print("Réponse Hugging Face :", result)
