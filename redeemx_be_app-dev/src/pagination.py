from fastapi import Query

def get_pagination_params(
    limit: int = Query(6, ge=1, description="Number of records per page"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
):
    return {"limit": limit, "offset": offset}
