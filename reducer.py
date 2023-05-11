from re import I


with open("input.txt", encoding="UTF-8") as f:
    text = f.read()

# remove every fifth character
# text = text[::5]

# remove every fifth character, starting from the fifth

words = text.split()

# remove every fifth word
for i in range(0, len(words), 5):
    try:
        words.pop(i)
    except IndexError:
        pass


text = ' '.join(words) 

with open("output.txt", "w", encoding="UTF-8") as f:
    f.write(text)