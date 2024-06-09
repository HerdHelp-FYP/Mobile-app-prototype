# import googletrans
# from googletrans import Translator

# # from translate import Translator

# prompt = "میری بھینس بیمار ہے."

# #User's prompt translation
# Translator= googletrans.Translator()
# translation = Translator.translate(prompt, src='ur', dest='en')
# prompttr_user = translation.text

# print("translation = ", prompttr_user)

import re

text = """As a Pakistani veterinarian, you provide expertise 
on livestock health and farming, assisting users with relevant queries. Here is some relevant context, My buffalo has a fever and is acting lethargic. What could be causing this fever? Fever and lethargy in buffalo could indicate infectious diseases like brucellosis or tuberculosis. question My buffalo 
is sick Now generate answer :-

**Possible causes of fever include:**
- Bacterial infections such as Brucella abortus (infectious abortion) or tuberculosis
 - Viral infections such as foot rot virus or bluetongue disease
 - Parasites such as roundworm or tapeworms
 - Metabolic disorders such as hypercalcaemia or hypoproteinemic anemia

Consult with a veterinarian for proper diagnosis and treatment."""

# Using re.DOTALL to include newlines
pattern = re.compile(r':-\s*(.*)', re.DOTALL)

# Search for the pattern in the text
match = pattern.search(text)

# If a match is found, print the captured group
if match:
    result = match.group(1)
    print("Captured text:", result)
else:
    print("Pattern not found.")