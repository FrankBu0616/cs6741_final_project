import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  engine="davinci-instruct-beta",
  prompt="Create turn-by-turn directions from this text:\n\nmove to the couch and turn left then move to the chair and then move to the plant\n\n1.",
  temperature=0,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
print(response["choices"])