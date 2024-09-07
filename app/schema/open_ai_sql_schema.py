from pydantic import BaseModel

# Define a Pydantic model for the request body
class QueryRequest_ai(BaseModel):
    query: str
    
# Define a Pydantic model for the request body
class SQLQueryRequest(BaseModel):
    query: str