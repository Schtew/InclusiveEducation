from openai import OpenAI
import os
import openai

api_key = os.environ.get("OPENAI_API_KEY")
print("API Key:", api_key)  

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

client.fine_tuning.jobs.create(
    training_file="data/cleandata.json",
    model="gpt-3.5-turbo"
)