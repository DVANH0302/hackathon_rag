
from sqlalchemy.orm import Session

from . import models, schemas 

def get_filename(db: Session, file_name: str):  
    return db.query(models.DocumentEmbedding).filter(models.DocumentEmbedding.file_name== file_name).first()

def add_document(db:Session, file: schemas.File):
    document_embedding = DocumentEmbedding(file_name = file.filename, content_type = file.content_type)
    db.add(document_embedding)
    db.flush()
    db.commit()
    return document_embedding
