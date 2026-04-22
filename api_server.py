from pathlib import Path
from typing import List, Optional
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents.memory import load_memory
from agents.pipeline import RUN_HISTORY_PATH, run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parent
WEB_ROOT = PROJECT_ROOT / "web"

app = FastAPI(
    title="Aerulias AI API",
    description="Self-improving multi-agent answer system with memory, refinement, and demo mode.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class PipelineRunRequest(BaseModel):
    query: str = Field(..., min_length=1)
    rounds: int = Field(default=2, ge=1, le=5)
    target: int = Field(default=90, ge=1, le=100)
    use_memory: bool = True
    source_paths: Optional[List[str] | str] = None
    demo_mode: bool = False
    save_outputs: bool = True


class PipelineRunResponse(BaseModel):
    result: dict


def load_history():
    if not RUN_HISTORY_PATH.exists():
        return []

    try:
        return json.loads(RUN_HISTORY_PATH.read_text())
    except json.JSONDecodeError:
        return []


def normalize_source_paths(source_paths):
    if not source_paths:
        return []

    if isinstance(source_paths, str):
        return [path.strip() for path in source_paths.splitlines() if path.strip()]

    return source_paths


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/pipeline/run", response_model=PipelineRunResponse)
def run_pipeline_endpoint(payload: PipelineRunRequest):
    try:
        result = run_pipeline(
            payload.query.strip(),
            max_rounds=payload.rounds,
            target_score=payload.target,
            use_memory=payload.use_memory,
            source_paths=normalize_source_paths(payload.source_paths),
            save_outputs=payload.save_outputs,
            demo_mode=payload.demo_mode
        )
        return {"result": result}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/demo/run", response_model=PipelineRunResponse)
def run_demo_endpoint(payload: PipelineRunRequest):
    payload.demo_mode = True
    payload.save_outputs = False
    return run_pipeline_endpoint(payload)


@app.get("/memory")
def memory():
    return {"memory": load_memory()[-20:]}


@app.get("/history")
def history():
    return {"history": load_history()[-20:]}


@app.get("/")
def dashboard():
    return FileResponse(WEB_ROOT / "index.html")


app.mount("/", StaticFiles(directory=WEB_ROOT), name="web")
