from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

app = FastAPI(
    title="Galactic Archives Store API",
    version="1.0.0",
)

# CORS – allow your static site domain
origins = [
    "https://galacticarchives.space",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Product(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    price: float
    currency: str = "GBP"
    category: Optional[str] = None
    is_active: bool = True
    external_id: Optional[str] = None  # e.g. Printful product id


# For now: static demo data so the frontend always gets multiple products.
# Later, you can replace this with a call to Printful or a database.
DEMO_PRODUCTS: List[Product] = [
    Product(
        id="prod_001",
        name="Holographic Stickers",
        description="A set of shimmering space-themed holographic stickers.",
        image_url="https://files.cdn.printful.com/path/to/holographic_stickers.png",
        price=4.99,
        category="Stickers",
        external_id="printful_123",
    ),
    Product(
        id="prod_002",
        name="Galactic Archives T-Shirt",
        description="Soft cotton t-shirt with the Galactic Archives emblem.",
        image_url="https://files.cdn.printful.com/path/to/galactic_archives_tshirt.png",
        price=18.50,
        category="Apparel",
        external_id="printful_456",
    ),
    Product(
        id="prod_003",
        name="Mission Patch",
        description="Embroidered mission patch for your flight suit or backpack.",
        image_url="https://files.cdn.printful.com/path/to/mission_patch.png",
        price=6.75,
        category="Accessories",
        external_id="printful_789",
    ),
]


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/products", response_model=List[Product])
def list_products(only_active: bool = True):
    """
    Return a flat array of products that the frontend can iterate over.
    """
    try:
        products = DEMO_PRODUCTS

        if only_active:
            products = [p for p in products if p.is_active]

        return products
    except Exception as e:
        # Log e in real code
        raise HTTPException(status_code=500, detail="Failed to fetch products")
