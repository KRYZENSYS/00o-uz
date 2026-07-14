"""CRM & Project Management API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Client, Deal, Task, Invoice, Project, ProjectMember, TimeEntry, Contract

router = APIRouter(prefix="/crm", tags=["crm"])


class ClientReq(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = []


class DealReq(BaseModel):
    client_id: int
    title: str
    amount: float
    currency: str = "UZS"
    stage: str = "lead"  # lead, qualified, proposal, negotiation, won, lost
    expected_close: Optional[datetime] = None
    notes: Optional[str] = None


class TaskReq(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    priority: str = "medium"  # low, medium, high, urgent
    due_date: Optional[datetime] = None


class InvoiceReq(BaseModel):
    client_id: int
    items: List[dict]  # [{name, qty, price}]
    due_date: datetime
    notes: Optional[str] = None


# ============ CLIENTS ============
@router.get("/clients")
async def list_clients(search: Optional[str] = None, limit: int = 100, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Client).where(Client.owner_id == user.id)
    if search: q = q.where(Client.name.ilike(f"%{search}%"))
    q = q.order_by(Client.created_at.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone, "company": c.company, "total_deals": c.total_deals, "created_at": c.created_at.isoformat()} for c in r.scalars().all()]


@router.post("/clients")
async def create_client(req: ClientReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = Client(owner_id=user.id, **req.dict())
    db.add(c); await db.commit(); await db.refresh(c)
    return {"id": c.id}


@router.get("/clients/{client_id}")
async def get_client(client_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    c = await db.get(Client, client_id)
    if not c or c.owner_id != user.id: raise HTTPException(404)
    return c


# ============ DEALS ============
@router.get("/deals")
async def list_deals(stage: Optional[str] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Deal).where(Deal.owner_id == user.id)
    if stage: q = q.where(Deal.stage == stage)
    q = q.order_by(Deal.created_at.desc())
    r = await db.execute(q)
    return [{"id": d.id, "title": d.title, "client_id": d.client_id, "amount": d.amount, "stage": d.stage, "expected_close": d.expected_close.isoformat() if d.expected_close else None, "created_at": d.created_at.isoformat()} for d in r.scalars().all()]


@router.post("/deals")
async def create_deal(req: DealReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    d = Deal(owner_id=user.id, **req.dict())
    db.add(d); await db.commit(); await db.refresh(d)
    return {"id": d.id}


@router.put("/deals/{deal_id}/stage")
async def update_deal_stage(deal_id: int, stage: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    d = await db.get(Deal, deal_id)
    if not d or d.owner_id != user.id: raise HTTPException(404)
    d.stage = stage
    if stage == "won": d.closed_at = datetime.utcnow(); d.status = "won"
    await db.commit()
    return {"stage": stage}


@router.get("/deals/pipeline")
async def deal_pipeline(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Kanban board view"""
    stages = ["lead", "qualified", "proposal", "negotiation", "won", "lost"]
    result = {}
    for s in stages:
        r = await db.execute(select(func.count(Deal.id), func.sum(Deal.amount)).where(Deal.owner_id == user.id, Deal.stage == s))
        count, total = r.first()
        result[s] = {"count": count or 0, "total": total or 0}
    return result


# ============ PROJECTS ============
@router.get("/projects")
async def list_projects(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Project).join(ProjectMember, ProjectMember.project_id == Project.id).where(ProjectMember.user_id == user.id)
    r = await db.execute(q)
    return [{"id": p.id, "name": p.name, "description": p.description, "status": p.status, "tasks_count": p.tasks_count, "completed_tasks": p.completed_tasks, "deadline": p.deadline.isoformat() if p.deadline else None} for p in r.scalars().all()]


@router.post("/projects")
async def create_project(name: str, description: str, deadline: Optional[datetime] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = Project(name=name, description=description, deadline=deadline, owner_id=user.id, status="active")
    db.add(p); await db.commit(); await db.refresh(p)
    db.add(ProjectMember(project_id=p.id, user_id=user.id, role="owner"))
    await db.commit()
    return {"id": p.id}


# ============ TASKS ============
@router.get("/tasks")
async def list_tasks(project_id: Optional[int] = None, status: Optional[str] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Task).where((Task.creator_id == user.id) | (Task.assignee_id == user.id))
    if project_id: q = q.where(Task.project_id == project_id)
    if status: q = q.where(Task.status == status)
    q = q.order_by(Task.due_date.asc().nullslast())
    r = await db.execute(q)
    return [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "due_date": t.due_date.isoformat() if t.due_date else None, "assignee_id": t.assignee_id} for t in r.scalars().all()]


@router.post("/tasks")
async def create_task(req: TaskReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    t = Task(creator_id=user.id, **req.dict(), status="todo")
    db.add(t); await db.commit(); await db.refresh(t)
    return {"id": t.id}


@router.put("/tasks/{task_id}/status")
async def update_task_status(task_id: int, status: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    t = await db.get(Task, task_id)
    if not t or t.creator_id != user.id: raise HTTPException(404)
    t.status = status
    if status == "done": t.completed_at = datetime.utcnow()
    await db.commit()
    return {"status": status}


# ============ INVOICES ============
@router.post("/invoices")
async def create_invoice(req: InvoiceReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    subtotal = sum(i.get("qty", 1) * i.get("price", 0) for i in req.items)
    inv = Invoice(owner_id=user.id, **req.dict(), subtotal=subtotal, total=subtotal, invoice_number=f"INV-{int(datetime.utcnow().timestamp())}", status="draft")
    db.add(inv); await db.commit(); await db.refresh(inv)
    return {"id": inv.id, "invoice_number": inv.invoice_number, "total": inv.total}


@router.get("/invoices")
async def list_invoices(status: Optional[str] = None, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Invoice).where(Invoice.owner_id == user.id)
    if status: q = q.where(Invoice.status == status)
    q = q.order_by(Invoice.created_at.desc())
    r = await db.execute(q)
    return [{"id": i.id, "invoice_number": i.invoice_number, "client_id": i.client_id, "total": i.total, "status": i.status, "due_date": i.due_date.isoformat()} for i in r.scalars().all()]


# ============ TIME TRACKING ============
@router.post("/time/start")
async def start_timer(task_id: Optional[int] = None, description: str = "", user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    te = TimeEntry(user_id=user.id, task_id=task_id, description=description, started_at=datetime.utcnow())
    db.add(te); await db.commit(); await db.refresh(te)
    return {"id": te.id, "started_at": te.started_at.isoformat()}


@router.post("/time/stop/{entry_id}")
async def stop_timer(entry_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    te = await db.get(TimeEntry, entry_id)
    if not te or te.user_id != user.id: raise HTTPException(404)
    te.ended_at = datetime.utcnow()
    te.duration = (te.ended_at - te.started_at).total_seconds() / 3600
    await db.commit()
    return {"duration_hours": te.duration}


# ============ ANALYTICS ============
@router.get("/analytics")
async def crm_analytics(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    clients = await db.scalar(select(func.count(Client.id)).where(Client.owner_id == user.id)) or 0
    deals_won = await db.scalar(select(func.count(Deal.id)).where(Deal.owner_id == user.id, Deal.stage == "won")) or 0
    revenue = await db.scalar(select(func.sum(Deal.amount)).where(Deal.owner_id == user.id, Deal.stage == "won")) or 0
    tasks_done = await db.scalar(select(func.count(Task.id)).where(Task.creator_id == user.id, Task.status == "done")) or 0
    return {"clients_count": clients, "deals_won": deals_won, "revenue": revenue, "tasks_completed": tasks_done}
