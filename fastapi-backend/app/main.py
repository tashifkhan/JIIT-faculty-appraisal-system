from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.endpoints import ingestion, faculty
from app.db.mongo import mongo_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    mongo_client.connect()
    yield
    # Shutdown
    mongo_client.close()


app = FastAPI(title="Faculty Appraisal System API", lifespan=lifespan)

# CORS Configuration
# Replicating Django's CORS_ALLOW_ALL_ORIGINS = True
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion.router, prefix="/api", tags=["ingestion"])
app.include_router(faculty.router, prefix="/api", tags=["faculty"])


@app.get("/")
def read_root():
    return {"message": "Faculty Appraisal System API is running"}
