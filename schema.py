from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class AnalysisOutput(BaseModel):
    answer:str
    chart_path:Optional[str] = ""
    query_sql:Optional[str] = ""
    data_preview: List[Dict] = Field(default_factory=list)

    


SYSTEM_PROMPT = f"""
You are a AI Data Analyst

**Workflow**
1. Parse user's Question.
2. If it's a numeric summary -> call `quick_stats`.
3. If filtering rows -> call `query_data`.
4. If trend request -> call `plot_timeseries`.
5. Always return JSON matching {AnalysisOutput.__name__} schema.

Never output anything except valid JSON
"""
