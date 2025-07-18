BETTER_WORD_PROMPT = """You need to output a JSON with the following structure:
{
  "text": "<text>"
}

The value <text> is the output obey the following rules:
1. Do not change the language of the text.
2. Fix the grammar and spelling mistakes.
3. Using constructive feedback, friendly and helpful tone, using advise rather than rhetorical question.
4. Respect and keep the original length of the text, do not over expanding.
5. Do not add punctuation 。/./etc.. at the end of a sentence unless the original sentence has it
6. If the original text sounds offensive, the revised version should soothe the recipient's feelings and, add more praise for them, in the end, encourage them to take action, and
... of the following given text between ``` and ```:
```
{original_text}
```

ONLY JSON IS ALLOWED as an answer. No explanation or other text is allowed."""
