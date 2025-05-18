from transformers import MarianTokenizer, MarianMTModel

langs = ['fr', 'de', 'hi']

for lang in langs:
    model_name = f'Helsinki-NLP/opus-mt-en-{lang}'
    MarianTokenizer.from_pretrained(model_name)
    MarianMTModel.from_pretrained(model_name)
