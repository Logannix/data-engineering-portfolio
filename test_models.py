from google import genai

client = genai.Client(api_key="AIzaSyDI8eODy7GtQ92fMdcSAxYOmN-rpClymwo")

models = client.models.list()

for m in models:
    print(m.name)