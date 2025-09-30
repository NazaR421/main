from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, Annotated
app=FastAPI()

library={}

class Book(BaseModel):
    title:str=Field(...,title="Назва книги",description="Назва книги повиннат бути",min_length=1 )
    author:str=Field(...,Title="Автор",description="імя автора",min_length=3,max_length=30)
    pages: int=Field(...,title="Кількість сторінок",description="Більше 10",gt=10)

@app.post("/books/",response_model=Book)
async def create_book(book:Book):
    author=book.author
    if author not in library:
        library[author] = []
    library[author].append(book)
    return book

@app.get("/books")
async def get_books(author=Query(...,title="Adnjh")):
    if author not in library:
        raise HTTPException(status_code=404,detail="автор не знайдений")
    return library[author]

@app.put("/books/")
async def update_book(book:Book):
    author=book.author
    if author not in library:
        raise HTTPException(status_code=404,detail="автор не знайдений")
    for b in library[author]:
        if b.title == book.title:
            b.pages == book.pages
            return {"Книга оновленна"}
        raise HTTPException(status_code=404,detail="Книга не знайдена")
    
@app.delete("/book/")
async def delete_book(title:str,author:str):
    if author not in library:
        raise HTTPException(status_code=404,detail="Книга не знайдена")
    for book in library[author]:
        if book.title == title:
            library[author].remove(book)
            return {"Книга видалена"}
    raise HTTPException(status_code=404,detail="Книга не знайдена")
        
