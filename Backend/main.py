from fastapi import FastAPI,Request
from pydantic import BaseModel
from transformers import MarianMTModel,MarianTokenizer
from fastapi.middleware.cors import CORSMiddleware

#The default Model is hugginFace
#The application will start supporting more models as time progresses
app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://babelmate-frontend.onrender.com","http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#How the input data should look like for /translate
class TranslationRequest(BaseModel):
    text : str
    target_lang: str
    model: str = "huggingface"

loaded_models = {}

#Transalation is now from english to any target language
#Over time this will start incoporating any lang - ang lang translation
def load_transalation_model(target_lang):
    model_name = f"Helsinki-NLP/opus-mt-en-{target_lang}"
    if target_lang not in loaded_models:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        loaded_models[target_lang] = (tokenizer,model)
    return loaded_models[target_lang]

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"message": "BabelMate Backend is up and running!"}

@app.post("/translate")
def translate(request: TranslationRequest):
    text = request.text
    target_lang = request.target_lang
    tokenizer,model = load_transalation_model(target_lang)

    inputs = tokenizer(text, return_tensors="pt",padding=True)
    translated = model.generate(**inputs)
    translated_text = tokenizer.decode(translated[0],skip_special_tokens=True)

    return {"translated_text": translated_text}




