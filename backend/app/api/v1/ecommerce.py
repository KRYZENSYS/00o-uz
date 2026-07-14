"""E-commerce / Marketplace API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, Product, ProductCategory, Order, OrderItem, Cart, CartItem, Review, Wishlist

router = APIRouter(prefix="/market", tags=["marketplace"])


class ProductCreateReq(BaseModel):
    name: str
    description: str
    category: str
    price: float
    old_price: Optional[float] = None
    currency: str = "UZS"
    images: List[str] = []
    stock: int = 1
    sku: Optional[str] = None
    brand: Optional[str] = None
    attributes: Optional[dict] = None
    is_digital: bool = False
    weight: Optional[float] = None


class CartItemReq(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreateReq(BaseModel):
    items: List[CartItemReq]
    shipping_address: str
    payment_method: str = "payme"
    notes: Optional[str] = None


class ReviewCreateReq(BaseModel):
    product_id: int
    rating: int
    text: str
    images: Optional[List[str]] = None


# ============ CATEGORIES ============
@router.get("/categories")
async def categories(db: AsyncSession = Depends(get_db)):
    return [
        {"id": "electronics", "name": "📱 Elektronika", "icon": "📱"},
        {"id": "fashion", "name": "👕 Kiyim", "icon": "👕"},
        {"id": "home", "name": "🏠 Uy-ro'zg'or", "icon": "🏠"},
        {"id": "beauty", "name": "💄 Go'zallik", "icon": "💄"},
        {"id": "sports", "name": "⚽ Sport", "icon": "⚽"},
        {"id": "kids", "name": "👶 Bolalar", "icon": "👶"},
        {"id": "books", "name": "📚 Kitoblar", "icon": "📚"},
        {"id": "auto", "name": "🚗 Avto", "icon": "🚗"},
        {"id": "food", "name": "🍎 Oziq-ovqat", "icon": "🍎"},
        {"id": "digital", "name": "💾 Raqamli", "icon": "💾"},
    ]


# ============ PRODUCTS ============
@router.get("/products")
async def list_products(category: Optional[str] = None, search: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None, sort: str = "newest", limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    q = select(Product).where(Product.is_active == True)
    if category: q = q.where(Product.category == category)
    if search: q = q.where(or_(Product.name.ilike(f"%{search}%"), Product.description.ilike(f"%{search}%")))
    if min_price: q = q.where(Product.price >= min_price)
    if max_price: q = q.where(Product.price <= max_price)
    if sort == "price_asc": q = q.order_by(Product.price)
    elif sort == "price_desc": q = q.order_by(Product.price.desc())
    elif sort == "popular": q = q.order_by(Product.sales_count.desc())
    else: q = q.order_by(Product.created_at.desc())
    q = q.limit(limit).offset(offset)
    r = await db.execute(q)
    return [{"id": p.id, "name": p.name, "price": p.price, "old_price": p.old_price, "currency": p.currency, "images": p.images, "rating": p.rating, "reviews_count": p.reviews_count, "sales_count": p.sales_count, "stock": p.stock, "discount": round((1 - p.price / p.old_price) * 100) if p.old_price and p.old_price > p.price else 0} for p in r.scalars().all()]


@router.get("/products/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    p = await db.get(Product, product_id)
    if not p: raise HTTPException(404)
    p.views_count += 1
    await db.commit()
    seller = await db.get(User, p.seller_id)
    
    # Reviews
    r = await db.execute(select(Review, User).join(User, User.id == Review.user_id).where(Review.product_id == product_id).order_by(Review.created_at.desc()).limit(20))
    reviews = [{"id": rv.id, "rating": rv.rating, "text": rv.text, "images": rv.images, "created_at": rv.created_at.isoformat(), "user": {"id": u.id, "full_name": u.full_name, "avatar_url": u.avatar_url}} for rv, u in r.all()]
    
    return {"id": p.id, "name": p.name, "description": p.description, "category": p.category, "price": p.price, "old_price": p.old_price, "currency": p.currency, "images": p.images, "stock": p.stock, "rating": p.rating, "reviews_count": p.reviews_count, "sales_count": p.sales_count, "brand": p.brand, "attributes": p.attributes, "is_digital": p.is_digital, "seller": {"id": seller.id, "full_name": seller.full_name, "avatar_url": seller.avatar_url, "rating": seller.rating}, "reviews": reviews}


@router.post("/products")
async def create_product(req: ProductCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = Product(seller_id=user.id, **req.dict())
    db.add(p); await db.commit(); await db.refresh(p)
    return {"id": p.id, "name": p.name}


@router.put("/products/{product_id}")
async def update_product(product_id: int, req: ProductCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.get(Product, product_id)
    if not p or p.seller_id != user.id: raise HTTPException(403)
    for k, v in req.dict().items(): setattr(p, k, v)
    await db.commit()
    return {"message": "Yangilandi"}


@router.delete("/products/{product_id}")
async def delete_product(product_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    p = await db.get(Product, product_id)
    if not p or p.seller_id != user.id: raise HTTPException(403)
    p.is_active = False
    await db.commit()
    return {"message": "O'chirildi"}


# ============ CART ============
@router.get("/cart")
async def get_cart(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Cart, CartItem, Product).join(CartItem, CartItem.cart_id == Cart.id).join(Product, Product.id == CartItem.product_id).where(Cart.user_id == user.id))
    items = []
    total = 0
    for c, ci, p in r.all():
        items.append({"id": ci.id, "product": {"id": p.id, "name": p.name, "images": p.images, "price": p.price}, "quantity": ci.quantity, "subtotal": ci.quantity * p.price})
        total += ci.quantity * p.price
    return {"items": items, "total": total, "items_count": len(items)}


@router.post("/cart/add")
async def add_to_cart(req: CartItemReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    cart = await db.scalar(select(Cart).where(Cart.user_id == user.id))
    if not cart: cart = Cart(user_id=user.id); db.add(cart); await db.commit(); await db.refresh(cart)
    
    existing = await db.scalar(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == req.product_id))
    if existing: existing.quantity += req.quantity
    else: db.add(CartItem(cart_id=cart.id, **req.dict()))
    await db.commit()
    return {"message": "Savatga qo'shildi"}


@router.delete("/cart/item/{item_id}")
async def remove_from_cart(item_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    item = await db.get(CartItem, item_id)
    if not item: raise HTTPException(404)
    cart = await db.get(Cart, item.cart_id)
    if not cart or cart.user_id != user.id: raise HTTPException(403)
    await db.delete(item); await db.commit()
    return {"message": "O'chirildi"}


@router.delete("/cart/clear")
async def clear_cart(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    cart = await db.scalar(select(Cart).where(Cart.user_id == user.id))
    if cart:
        await db.execute(CartItem.__table__.delete().where(CartItem.cart_id == cart.id))
        await db.commit()
    return {"message": "Savat tozalandi"}


# ============ ORDERS ============
@router.post("/orders")
async def create_order(req: OrderCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not req.items: raise HTTPException(400, "Savat bo'sh")
    
    total = 0
    order = Order(user_id=user.id, shipping_address=req.shipping_address, payment_method=req.payment_method, notes=req.notes, status="pending", total=0)
    db.add(order); await db.commit(); await db.refresh(order)
    
    for item in req.items:
        product = await db.get(Product, item.product_id)
        if not product or product.stock < item.quantity: raise HTTPException(400, f"'{product.name if product else '?'}' yetarli emas")
        product.stock -= item.quantity
        product.sales_count += item.quantity
        db.add(OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=product.price))
        total += product.price * item.quantity
    
    order.total = total
    await db.commit()
    
    # Process payment (Payme, Click, etc.)
    return {"id": order.id, "total": total, "status": "pending_payment", "payment_url": f"https://pay.00o.uz/order/{order.id}"}


@router.get("/orders")
async def my_orders(status: Optional[str] = None, limit: int = 50, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Order).where(Order.user_id == user.id)
    if status: q = q.where(Order.status == status)
    q = q.order_by(Order.created_at.desc()).limit(limit)
    r = await db.execute(q)
    return [{"id": o.id, "total": o.total, "status": o.status, "items_count": o.items_count, "created_at": o.created_at.isoformat()} for o in r.scalars().all()]


@router.get("/orders/{order_id}")
async def get_order(order_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    o = await db.get(Order, order_id)
    if not o or o.user_id != user.id: raise HTTPException(404)
    r = await db.execute(select(OrderItem, Product).join(Product, Product.id == OrderItem.product_id).where(OrderItem.order_id == order_id))
    items = [{"id": oi.id, "product": {"id": p.id, "name": p.name, "images": p.images}, "quantity": oi.quantity, "price": oi.price, "subtotal": oi.quantity * oi.price} for oi, p in r.all()]
    return {"id": o.id, "total": o.total, "status": o.status, "shipping_address": o.shipping_address, "items": items, "tracking_number": o.tracking_number, "created_at": o.created_at.isoformat()}


@router.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    o = await db.get(Order, order_id)
    if not o or o.user_id != user.id: raise HTTPException(404)
    if o.status not in ["pending", "pending_payment"]: raise HTTPException(400, "Bekor qilib bo'lmaydi")
    o.status = "cancelled"
    await db.commit()
    return {"message": "Bekor qilindi"}


@router.post("/orders/{order_id}/pay")
async def pay_order(order_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Mark order as paid (after payment gateway callback)"""
    o = await db.get(Order, order_id)
    if not o or o.user_id != user.id: raise HTTPException(404)
    o.status = "paid"
    o.paid_at = datetime.utcnow()
    await db.commit()
    return {"message": "To'lov qabul qilindi"}


# ============ REVIEWS ============
@router.post("/reviews")
async def create_review(req: ReviewCreateReq, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if req.rating < 1 or req.rating > 5: raise HTTPException(400, "Rating 1-5")
    rv = Review(user_id=user.id, **req.dict())
    db.add(rv)
    
    # Update product rating
    p = await db.get(Product, req.product_id)
    if p:
        total = (p.rating or 0) * (p.reviews_count or 0) + req.rating
        p.reviews_count = (p.reviews_count or 0) + 1
        p.rating = total / p.reviews_count
    await db.commit()
    return {"id": rv.id, "rating": rv.rating}


# ============ WISHLIST ============
@router.get("/wishlist")
async def my_wishlist(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Wishlist, Product).join(Product, Product.id == Wishlist.product_id).where(Wishlist.user_id == user.id))
    return [{"id": w.id, "product": {"id": p.id, "name": p.name, "price": p.price, "images": p.images}} for w, p in r.all()]


@router.post("/wishlist/toggle/{product_id}")
async def toggle_wishlist(product_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(Wishlist).where(Wishlist.user_id == user.id, Wishlist.product_id == product_id))
    if existing:
        await db.delete(existing); await db.commit()
        return {"added": False}
    db.add(Wishlist(user_id=user.id, product_id=product_id)); await db.commit()
    return {"added": True}


# ============ SELLER DASHBOARD ============
@router.get("/seller/dashboard")
async def seller_dashboard(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    products = await db.scalar(select(func.count(Product.id)).where(Product.seller_id == user.id)) or 0
    orders = await db.scalar(select(func.count(Order.id)).where(Order.seller_id == user.id)) or 0
    revenue = await db.scalar(select(func.sum(Order.total)).where(Order.seller_id == user.id, Order.status == "delivered")) or 0
    rating = await db.scalar(select(func.avg(Review.rating)).join(Product, Product.id == Review.product_id).where(Product.seller_id == user.id)) or 0
    return {"products_count": products, "orders_count": orders, "revenue": revenue, "rating": round(rating, 1)}
