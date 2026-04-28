from pathlib import Path
from typing import List, Optional
import json
import logging
import sys
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents.memory import load_memory
from agents.pipeline import RUN_HISTORY_PATH, run_pipeline

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent
WEB_ROOT = PROJECT_ROOT / "web"

logger.info(f"Aerulias AI API starting - Project root: {PROJECT_ROOT}")

app = FastAPI(
    title="Aerulias AI API",
    description="Self-improving multi-agent answer system with memory, refinement, and demo mode.",
    version="1.1.0"
)

# ===== CORS CONFIGURATION =====
allowed_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# Allow Render domain from environment
render_url = os.getenv("RENDER_EXTERNAL_URL")
if render_url:
    allowed_origins.append(render_url)
    logger.info(f"Added Render URL to CORS: {render_url}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if not os.getenv("ENV") == "production" else ["*"],
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
    logger.info("Health check received")
    return {"status": "ok", "version": "1.1.0"}


@app.post("/pipeline/run", response_model=PipelineRunResponse)
def run_pipeline_endpoint(payload: PipelineRunRequest):
    try:
        logger.info(f"Pipeline run requested: query='{payload.query[:50]}...', rounds={payload.rounds}, demo={payload.demo_mode}")
        
        result = run_pipeline(
            payload.query.strip(),
            max_rounds=payload.rounds,
            target_score=payload.target,
            use_memory=payload.use_memory,
            source_paths=normalize_source_paths(payload.source_paths),
            save_outputs=payload.save_outputs,
            demo_mode=payload.demo_mode
        )
        
        logger.info(f"Pipeline completed successfully with final score: {result.get('final_score', 'N/A')}")
        return {"result": result}
    except Exception as error:
        logger.error(f"Pipeline execution error: {str(error)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/demo/run", response_model=PipelineRunResponse)
def run_demo_endpoint(payload: PipelineRunRequest):
    try:
        logger.info("Demo run requested")
        payload.demo_mode = True
        payload.save_outputs = False
        return run_pipeline_endpoint(payload)
    except Exception as error:
        logger.error(f"Demo execution error: {str(error)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/memory")
def memory():
    try:
        mem = load_memory()
        logger.info(f"Memory endpoint called - {len(mem)} items")
        return {"memory": mem[-20:]}
    except Exception as error:
        logger.error(f"Memory endpoint error: {str(error)}", exc_info=True)
        return {"memory": []}


@app.get("/history")
def history():
    try:
        hist = load_history()
        logger.info(f"History endpoint called - {len(hist)} items")
        return {"history": hist[-20:]}
    except Exception as error:
        logger.error(f"History endpoint error: {str(error)}", exc_info=True)
        return {"history": []}


@app.get("/")
def dashboard():
    try:
        index_path = WEB_ROOT / "index.html"
        if not index_path.exists():
            logger.warning(f"index.html not found at {index_path}")
            raise FileNotFoundError(f"Dashboard not found at {index_path}")
        logger.info("Dashboard requested")
        return FileResponse(index_path)
    except Exception as error:
        logger.error(f"Dashboard error: {str(error)}", exc_info=True)
        raise HTTPException(status_code=404, detail="Dashboard not found") from error


# ===== STATIC FILES =====
try:
    app.mount("/", StaticFiles(directory=WEB_ROOT, check_dir=False), name="web")
    logger.info(f"Static files mounted from {WEB_ROOT}")
except Exception as error:
    logger.warning(f"Failed to mount static files: {str(error)}")


# ===== STARTUP EVENT =====
@app.on_event("startup")
async def startup_event():
    logger.info("Aerulias AI API startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Aerulias AI API shutting down")
