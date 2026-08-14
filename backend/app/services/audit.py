from uuid import UUID
from sqlalchemy.orm import Session
from app.models import AuditLog

def record(db: Session, action: str, entity_type: str, entity_id: UUID, details: dict | None = None) -> None:
    db.add(AuditLog(action=action, entity_type=entity_type, entity_id=entity_id, details=details))
