import openai
output = openai.Completion.create(
    model="curie:ft-cornell-university-2-2021-12-07-18-26-34",
    prompt="move to the trashcan and turn right, then move to the door\n\n1.")

print(output)
