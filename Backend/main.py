from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer
import torch

app = FastAPI()

# Allow CORS for all origins - you can restrict origins here if you want
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supported languages
LANGS = ['fr', 'de', 'es', 'hi', 'zh', 'ar', 'jap', 'vi']

# Load all models and tokenizers into memory (cached)
MODEL_CACHE = {}

for lang in LANGS:
    try:
        model_name = f"Helsinki-NLP/opus-mt-en-{lang}"
        print(f"Loading tokenizer and model for: {lang}")
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        MODEL_CACHE[lang] = {
            "tokenizer": tokenizer,
            "model": model
        }
        print(f"✅ Loaded: {model_name}")
    except Exception as e:
        print(f"❌ Error loading {lang}: {e}")

# Request schema for POST
class TranslationRequest(BaseModel):
    text: str
    target_lang: str
    model: str = "huggingface"  # optional

@app.get("/")
async def root():
    return {"message": "BabelMate Backend is up and running!"}

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    text = request.text
    target_lang = request.target_lang

    if target_lang not in MODEL_CACHE:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {target_lang}")

    tokenizer = MODEL_CACHE[target_lang]["tokenizer"]
    model = MODEL_CACHE[target_lang]["model"]

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        translated = model.generate(**inputs)
    output = tokenizer.decode(translated[0], skip_special_tokens=True)

    return {"translated_text": output}

# Support GET /translate?text=...&target_lang=...
@app.get("/translate")
async def translate_get(text: str, target_lang: str):
    if target_lang not in MODEL_CACHE:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {target_lang}")

    tokenizer = MODEL_CACHE[target_lang]["tokenizer"]
    model = MODEL_CACHE[target_lang]["model"]

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        translated = model.generate(**inputs)
    output = tokenizer.decode(translated[0], skip_special_tokens=True)

    return {"translated_text": output}

# HEAD requests are handled automatically by FastAPI and Starlette for these routes

