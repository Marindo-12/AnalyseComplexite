
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from program_analyzer import analyze_program


app = FastAPI(
    title="AnalyseComplexite API",
    description=(
        "API qui estime la complexité temporelle "
        "et spatiale d'un programme Python."
    ),
    version="0.1.0",
)


class AnalyzeRequest(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=50000,
        description="Code Python à analyser",
    )
    language: str = Field(
        default="python",
        description="Langage du code source",
    )


@app.get("/")
def home():
    return {
        "message": "Bienvenue sur l'API AnalyseComplexite",
        "documentation": "/docs",
        "endpoint": "POST /analyze",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if request.language.lower() != "python":
        raise HTTPException(
            status_code=400,
            detail="Pour le moment, seul Python est supporté.",
        )

    try:
        return analyze_program(request.code)

    except (ValueError, NotImplementedError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
