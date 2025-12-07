from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Galactic Archives Store API")

# Configure CORS to allow requests from your GitHub Pages site
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://galactic-archives.github.io",
                "https://galacticarchives.space",
        "http://localhost:*",
        "http://127.0.0.1:*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get Printful API key from environment variable
PRINTFUL_API_KEY = os.getenv("PRINTFUL_API_KEY")
PRINTFUL_BASE_URL = "https://api.printful.com"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Galactic Archives Store API",
        "message": "API proxy for Printful integration"
    }

@app.get("/api/products")
async def get_products():
    """Fetch all products from Printful"""
    if not PRINTFUL_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Printful API key not configured"
        )
    
    headers = {
        "Authorization": f"Bearer {PRINTFUL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{PRINTFUL_BASE_URL}/products",
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Printful API error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching products: {str(e)}"
        )

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """Fetch a specific product from Printful"""
    if not PRINTFUL_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Printful API key not configured"
        )
    
    headers = {
        "Authorization": f"Bearer {PRINTFUL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{PRINTFUL_BASE_URL}/products/{product_id}",
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Printful API error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching product: {str(e)}"
        )
