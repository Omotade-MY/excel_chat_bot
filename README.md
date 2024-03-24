# excel_chat_bot

Set up you openai api key

```os.environ["OPENAI_API_KEY"] == ...```
to run the code

```pip install -r requirements.txt```
```uvicorn app:app```

The API endpoint should be at ```http://127.0.0.1:8000/chat/{user prompt here}```