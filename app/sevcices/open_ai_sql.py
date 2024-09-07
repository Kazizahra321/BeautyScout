import openai
import os
Resource=os.environ.get('AzureOpenAIResource')
OPENAI_API_KEY = os.environ.get('AzureOpenAIKey')
OPENAI_API_TYPE = "azure"
OPENAI_API_BASE = f"https://{Resource}.openai.azure.com"
OPENAI_API_VERSION = "2023-03-15-preview"
MODEL_DEPLOYMENT_NAME = 'deployment-gpt-35-turbo-16k'

openai.api_type = "azure"
openai.api_base = OPENAI_API_BASE
openai.api_version = OPENAI_API_VERSION
openai.api_key = OPENAI_API_KEY

def get_sql(search_query):

    prompt=f'''So here is the row of the container in Cosmos .
        description of column:
        makeup_id: A unique identifier for each makeup product.
        name: The specific name of the product, such as "Maybelline Fit Me Foundation."
        brand: The brand name associated with the product, like "Maybelline" or "MAC."
        category: The type of makeup product, such as "Foundation," "Lipstick," "Blush," etc.
        price: The price of the product in USD.
        rating: The customer rating of the product on a scale of 1 to 5.
        color: The shade or color of the product, such as "Natural Beige" or "Ruby Woo."
        description: A brief description of the product, highlighting its features, like "A lightweight foundation that provides a flawless finish."
        image: The filename of an image representing the product.

        categories = [
            "Foundation", "Lipstick", "Blush", "Foundation", "Mascara",
            "Eyeshadow", "Eyebrow Pencil", "Lipstick", "Concealer",
            "Setting Powder", "Bronzer", "Mascara", "Setting Powder",
            "Foundation", "Lip Gloss", "Primer", "Moisturizer", "Foundation",
            "Concealer", "Primer"
        ]
        
        brands = [
            "Maybelline", "MAC", "NARS", "Fenty Beauty", "Too Faced",
            "Urban Decay", "Anastasia Beverly Hills", "Huda Beauty",
            "Tarte", "Charlotte Tilbury", "Benefit", "Dior",
            "Laura Mercier", "Giorgio Armani", "Fenty Beauty",
            "Smashbox", "Clinique", "Lancome", "Yves Saint Laurent",
            "Bobbi Brown"
        ]
        
        names = [
    "Maybelline Fit Me Foundation", "MAC Matte Lipstick",
    "NARS Blush", "Fenty Beauty Pro Filt'r Foundation",
    "Too Faced Better Than Sex Mascara", "Urban Decay Naked Eyeshadow Palette",
    "Anastasia Beverly Hills Brow Wiz", "Huda Beauty Liquid Matte Lipstick",
    "Tarte Shape Tape Concealer", "Charlotte Tilbury Airbrush Flawless Finish Setting Powder",
    "Benefit Cosmetics Hoola Bronzer", "Dior Diorshow Waterproof Mascara",
    "Laura Mercier Translucent Loose Setting Powder", "Giorgio Armani Luminous Silk Foundation",
    "Fenty Beauty Gloss Bomb Universal Lip Luminizer",
    "Smashbox Photo Finish Foundation Primer", "Clinique Moisture Surge 72-Hour Auto-Replenishing Hydrator",
    "Lancome Teint Idole Ultra Wear Foundation", "Yves Saint Laurent Touche Eclat Radiant Touch",
    "Bobbi Brown Vitamin Enriched Face Base"
]

        
        row={{{{
        "makeup_id": "1",
        "name": "Maybelline Fit Me Foundation",
        "brand": "Maybelline",
        "category": "Foundation",
        "price": 7.99,
        "rating": 4.5,
        "color": "Natural Beige",
        "description": "A lightweight foundation that provides a flawless finish and matches natural skin tone."}}}}
        
        write a Cosmos sql query to get the data from the container from the given Query.
        FOr example: SELECT * FROM c where c.makeup_id = '2'
        Query: {search_query}.
        
        Rules:
        1. Only Give the query and nothing else not even ;.
    '''

    response = openai.ChatCompletion.create(
                engine="deployment-gpt-35-turbo-16k",
                messages=[{'role': 'system', 'content': 'You are a helpfull assitant'},{'role': 'user', 'content': prompt}],
                temperature=0.1,
                max_tokens=1500,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
    
    return response['choices'][0]['message']['content']