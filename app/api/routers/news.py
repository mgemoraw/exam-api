from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate, NewsResponse
from app.infrastructure.database import get_db

news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)

@news_router.get("/", response_model=list[NewsResponse])
async def get_all_news(db: Session = Depends(get_db)):
    news_items = db.query(News).all()
    return news_items

@news_router.get("/{news_id}", response_model=NewsResponse)
async def get_news(news_id: str, db: Session = Depends(get_db)):
    news_item = db.query(News).filter(News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="News item not found")
    return news_item

@news_router.post("/", response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
async def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    new_news = News(
        title=news.title,
        content=news.content,
        created_by="system"  # Replace with actual user ID from auth context
    )
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return new_news

@news_router.put("/{news_id}", response_model=NewsResponse)
async def update_news(news_id: str, news_update: NewsUpdate, db: Session = Depends(get_db)):
    news_item = db.query(News).filter(News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="News item not found")
    
    if news_update.title is not None:
        news_item.title = news_update.title
    if news_update.content is not None:
        news_item.content = news_update.content
    
    db.commit()
    db.refresh(news_item)
    return news_item 

@news_router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(news_id: str, db: Session = Depends(get_db)):
    news_item = db.query(News).filter(News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="News item not found")
    
    db.delete(news_item)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


