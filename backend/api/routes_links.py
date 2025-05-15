from fastapi import APIRouter, Depends, HTTPException
from ..db.mongodb import get_database
from ..models import links as link_model
from ..schemas import links as link_schema

router = APIRouter(prefix="/api/links", tags=["Links"])

@router.get("/", response_model=list[link_schema.LinkOut])
async def read_all_links(db=Depends(get_database)):
    return await link_model.get_all_links(db)

@router.get("/{id}", response_model=link_schema.LinkOut)
async def read_link(id: str, db=Depends(get_database)):
    link = await link_model.get_link_by_id(db, id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@router.post("/", response_model=str)
async def create_link(link: link_schema.LinkCreate, db=Depends(get_database)):
    return await link_model.create_link(db, link.dict())

@router.delete("/{id}")
async def delete_link(id: str, db=Depends(get_database)):
    await link_model.delete_link(db, id)
    return {"message": "Link deleted successfully"}
