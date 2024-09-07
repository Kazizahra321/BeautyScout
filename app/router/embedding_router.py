from fastapi import FastAPI, Request, Form, Response, APIRouter,HTTPException
from fastapi.responses import JSONResponse
from ..schema.demo_schema import QueryRequest
from ..sevcices.open_ai_sql import get_sql
from ..schema.open_ai_sql_schema import QueryRequest_ai,SQLQueryRequest
import logging
from azure.cosmos import CosmosClient, exceptions

url = 'https://makeupcosmos.documents.azure.com:443/'  # Replace with your Cosmos DB account URL
key = 'X7farQPzXdrEbqj87avAD3Th95L9vuNx80PDiBmp5hMADfsZZ3VZYkzsYFuOI6sEViIjxZ5jndaCACDbTt5lxg=='  # Replace with your Cosmos DB account key
client = CosmosClient(url, key)

# Select the database and container
database_name = "Makeup_db"
container_name = "Makeup_container"
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)


router = APIRouter()
        
@router.post("/api/get_query")
async def get_sql_query(QueryRequest: QueryRequest_ai):
    query_string = QueryRequest.query
    try:
        sql = get_sql(query_string)
        return sql
    except Exception as e:
        logging.exception("health_check api failed")
        
@router.post("/api/get_data_from_sql_query")       
async def execute_cosmos_query(query_request: SQLQueryRequest):
    query = query_request.query
    try:
        # Execute the query and fetch results
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return {"results": items}
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
        

@router.post("/api/get_data_from_query_string")
async def get_data_from_query_string(query_request: QueryRequest_ai):
    query_string = query_request.query
    try:
        # Convert query string to SQL (synchronous call, no await needed)
        sql_query = get_sql(query_string)  # No await here
        
        # Execute the SQL query and fetch results from Cosmos DB
        items = list(container.query_items(
            query=sql_query,
            enable_cross_partition_query=True
        ))
        
        return {"results": items}
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logging.exception("Error occurred while processing the request")
        raise HTTPException(status_code=400, detail=str(e))
