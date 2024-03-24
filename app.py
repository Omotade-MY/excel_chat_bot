from main import Analyst, get_ggsheet, llm
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import io

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
class File(BaseModel):
    file: bytes

from dotenv import load_dotenv
_ = load_dotenv



#agent_exec.run("what is the asset with the highest price")


app = FastAPI(title="Excel Chat bot")

#@app.post("/upload/", response_model=Answer)
#async def loadfile(file: File):
#    answer = query_llm(question.question)
#    return {"answer": answer}


@app.get("/chat/{question}", response_model=Answer)
async def get_response(question: str):
    analyst_agent = Analyst('PortfolioData.xlsx', llm)

    agent_exec = analyst_agent.initialize()
    answer = agent_exec.run(question)
    return {"answer": answer}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"message": exc.detail}


