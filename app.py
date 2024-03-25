
from main import Analyst, get_ggsheet, llm, get_file_infomation
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import io
import pandas as pd
from dotenv import load_dotenv
_ = load_dotenv()


class Question(BaseModel):
    question: str

class Response(BaseModel):
    response: dict


app = FastAPI(title="Excel Chat bot")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(None), sheet_link: str = Form(None)):
    # Check if the uploaded file is of allowed types
    if file:
        allowed_extensions = {'csv', 'xlsx'}
        file_extension = file.filename.split(".")[-1]
        if file_extension.lower() not in allowed_extensions:
            return JSONResponse(status_code=400, content={"message": "Unsupported file type"})

        # Save the file to a temporary location or perform further processing
        file_contents = await file.read()
        file_like_object = io.BytesIO(file_contents)
    #print(file.getvalue())
    # You can save the file to disk, process it, etc.
        info = {"filename": file.filename, "file_extension": file_extension}
        if file_extension == "csv":

            df = pd.read_csv(file_like_object)
            info = info | get_file_infomation(df)
            df.to_csv("uploaded.csv", index=False)
        else:
            df = pd.read_excel(file_like_object, engine='openpyxl')
            info =  info | get_file_infomation(df)
            df.to_csv("uploaded.csv", index=False)
    elif sheet_link:
        url = get_ggsheet(sheet_link)
        df = pd.read_csv(url)
        df.to_csv("uploaded.csv", index=False)
        info = {'File Source': 'Google sheet'} | get_file_infomation(df)

    return info
    

@app.post("/chat/", response_model=Response)
async def get_response(question: str):
    analyst_agent = Analyst('uploaded.csv',llm)
    agent_exec = analyst_agent.initialize()
    response = agent_exec.run(question)
    return {"response": response}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"message": exc.detail}
