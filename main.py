from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import httpx
import os

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

# Get Printful API key from environment variable
PRINTFUL_API_KEY = os.getenv("PRINTFUL_API_KEY")
if not PRINTFUL_API_KEY:
    raise ValueError("PRINTFUL_API_KEY environment variable is not set")

PRINTFUL_API_BASE = "https://api.printful.com"


class Product(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    price: float
    currency: str = "GBP"
    category: Optional[str] = None
    is_active: bool = True
    external_id: Optional[str] = None  # Printful product id


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


async def fetch_printful_products():
    """
    Fetch products from Printful API.
    This fetches sync products (products you've synced to your store).
    """
    headers = {
        "Authorization": f"Bearer {PRINTFUL_API_KEY}",
        "Content-Type": "application/json",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Fetch sync products from Printful
            response = await client.get(
                f"{PRINTFUL_API_BASE}/store/products",
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Printful API error: {data.get('result')}"
                )
            
            return data.get("result", [])
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch products from Printful: {str(e)}"
            )


def map_printful_product_to_product(printful_product: dict) -> Product:
    """
    Map a Printful sync product to our Product model.
    """
    sync_product = printful_product.get("sync_product", {})
    sync_variants = printful_product.get("sync_variants", [])
    
    # Get the first variant for pricing (you can customize this logic)
    first_variant = sync_variants[0] if sync_variants else {}
    retail_price = first_variant.get("retail_price", "0")
    currency = first_variant.get("currency", "GBP")
    
    # Get thumbnail image
    thumbnail_url = sync_product.get("thumbnail_url")
    
    return Product(
        id=str(sync_product.get("id")),
        name=sync_product.get("name", "Unknown Product"),
        description=sync_product.get("name", ""),
        image_url=thumbnail_url,
        price=float(retail_price),
        currency=currency,
        category="Products",
        is_active=True,
        external_id=str(sync_product.get("id"))
    )


@app.get("/api/products", response_model=List[Product])
async def list_products(only_active: bool = True):
    """
    Return a flat array of products from Printful that the frontend can iterate over.
    """
    try:
        printful_products = await fetch_printful_products()
        
        # Map Printful products to our Product model
        products = [
            map_printful_product_to_product(p)
            for p in printful_products
        ]
        
        if only_active:
            products = [p for p in products if p.is_active]
        
        return products
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch products: {str(e)}"
        )
