
# excel_chat_bot

Set up you openai api key

```os.environ["OPENAI_API_KEY"] == ...```\

to run the code

```pip install -r requirements.txt```

Run the below code to start the uvicorn server

```uvicorn app:app```


The API endpoint should be at ```http://localhost:8000/chat/```


### Uploading a File
- **Endpoint:** `POST /upload/`
- **Parameters:**
  - `file`: Upload a CSV file.
  - `sheet_link`: Provide a Google Sheet link.
- **Response:** Information about the uploaded file or Google Sheet.

#### Example using `curl` for uploading a CSV file:
```bash
curl -X POST -F "file=@/path/to/your/file.csv" http://localhost:8000/upload/
```

#### Example using `curl` for providing a Google Sheet link:
```bash
curl -X POST -d "sheet_link=your_google_sheet_link" http://localhost:8000/upload/
```

### Getting a Response from Chatbot
- **Endpoint:** `POST /chat/`
- **Parameters:**
  - `question`: Question to ask the chatbot.
- **Response:** Chatbot's response to the question.

#### Example using `curl` for getting a response:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"question": "Your question here"}' http://localhost:8000/chat/
```

### Error Handling
- The API provides basic error handling for invalid requests or errors during processing.
- If an error occurs, the API will return a JSON response with an appropriate error message.

This documentation outlines how to access each endpoint of your FastAPI application. You can use tools like `curl` or Postman to send HTTP requests and interact with the API. Make sure to replace `http://localhost:8000` with the appropriate URL where your FastAPI server is running.

# JAVASCRIPT
**Uploading a File**

```javascript
// Upload a CSV file
const fileInput = document.querySelector('input[type="file"]');
const url = 'http://localhost:8000/upload/';
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch(url, {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

// Provide a Google Sheet link
const sheetLink = 'your_google_sheet_link';
fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: `sheet_link=${encodeURIComponent(sheetLink)}`
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```


**Getting a Response from Chatbot**\

```javascript
const url = 'http://localhost:8000/chat/';
const question = 'Your question here';

fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: question })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## PYTHON

**Uploading a Fiele**\

```python
import requests

# Upload a CSV file
file_path = '/path/to/your/file.csv'
url = 'http://localhost:8000/upload/'
files = {'file': open(file_path, 'rb')}
response = requests.post(url, files=files)
print(response.json())

# Provide a Google Sheet link
sheet_link = 'your_google_sheet_link'
response = requests.post(url, data={'sheet_link': sheet_link})
print(response.json())

```

**Getting Response from chatbot**\
```python
import requests


headers = {'accept': 'application/json'}
question = "what is the asset with the highest value"
url = f'http://localhost:8000/chat/?question={question}'

response = requests.post(url, headers=headers)
print(response.json())

```