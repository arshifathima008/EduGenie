from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Literal

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# ---------------------------------------------------------
# Static files and templates
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class ExplainRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"

    weeks: int = Field(
        default=6,
        ge=1,
        le=52
    )


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

@app.post("/qa")
async def qa(payload: QuestionRequest):

    answer = await answer_question(
        payload.question
    )

    return {
        "answer": answer
    }


# ---------------------------------------------------------
# Explanation
# ---------------------------------------------------------

@app.post("/explain")
async def explain(payload: ExplainRequest):

    explanation = await explain_topic(
        payload.topic
    )

    return {
        "explanation": explanation
    }


# ---------------------------------------------------------
# Quiz
# ---------------------------------------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    return await generate_quiz(
        payload.text
    )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    summary = await summarize_text(
        payload.text
    )

    return {
        "summary": summary
    }


# ---------------------------------------------------------
# Learning Path
# ---------------------------------------------------------

@app.post("/learn/recommendations")
async def learning_path(
    payload: LearningPathRequest
):

    return await get_learning_recommendations(
        topic=payload.topic,
        level=payload.level,
        weeks=payload.weeks
    )