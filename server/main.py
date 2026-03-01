import json
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import models
from core_algorithm import core_algorithm_v1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExperimentData(BaseModel):
    title: str
    quantumN: int
    mappings: List[dict]

@app.post("/optimize")
async def run_optimization(exp: ExperimentData):
    targets = [int(item['target']) for item in exp.mappings]
    
    # 直接將 generator 函式傳入 StreamingResponse
    # media_type 設為 text/event-stream 符合 SSE (Server-Sent Events) 規範
    return StreamingResponse(
        core_algorithm_v1(targets, exp.quantumN), 
        media_type="text/event-stream"
    )

# Dependency: 獲取資料庫 Session
def get_db():
    db = models.SessionLocal()
    try: yield db
    finally: db.close()

@app.post("/experiments")
def create_experiment(exp: ExperimentData, db: Session = Depends(get_db)):
    # 將 mappings 陣列轉換成您要的 TXT/CSV 格式字串
    txt_content = "\n".join([f"{item['input']},{item['target']}" for item in exp.mappings])
    
    new_exp = models.Experiment(
        title=exp.title, 
        quantumN=exp.quantumN,
        input_data=txt_content # 儲存如同 TXT 的格式
    )
    db.add(new_exp)
    db.commit()
    db.refresh(new_exp)
    return {"id": new_exp.id}

@app.post("/optimize/{exp_id}")
async def run_optimization(exp_id: int, exp: ExperimentData, db: Session = Depends(get_db)):
    targets = [int(item['target']) for item in exp.mappings]
    
    # 定義一個包裝過的產生器，負責在最後將結果存回資料庫
    async def save_and_stream():
        final_circuit = None
        async for chunk in core_algorithm_v1(targets, exp.quantumN):
            # 解析並記錄最終結果
            if "data: " in chunk:
                data = json.loads(chunk.replace("data: ", ""))
                if "circuit" in data:
                    final_circuit = data["circuit"]
            yield chunk
        
        # 迭代完成後存入 DB
        db_exp = db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()
        if db_exp:
            db_exp.circuit_data = json.dumps(final_circuit)
            db.commit()

    return StreamingResponse(save_and_stream(), media_type="text/event-stream")

# 您要求的 CRUD API
@app.get("/experiments")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Experiment).all()

@app.delete("/experiments")
def delete_all(db: Session = Depends(get_db)):
    db.query(models.Experiment).delete()
    db.commit()
    return {"status": "success"}

@app.get("/experiments/{exp_id}")
def get_experiment_detail(exp_id: int, db: Session = Depends(get_db)):
    # 提取特定實驗的所有數據
    return db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)