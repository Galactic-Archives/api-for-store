# api-for-store

FastAPI backend proxy for Galactic Archives store - Secure Printful API integration

## Overview

This is a backend API proxy that securely handles Printful API requests for the Galactic Archives store frontend. It keeps API keys secure by storing them as environment variables rather than exposing them in client-side code.

## Features

- 🔒 **Secure API Key Management**: API keys stored as environment variables, never exposed to frontend
- 🌐 **CORS Enabled**: Configured for GitHub Pages deployment
- ⚡ **Async Performance**: Uses httpx async client for fast API calls
- 🛡️ **Error Handling**: Comprehensive error handling for API failures
- 📊 **Health Check**: Status endpoint for monitoring

## API Endpoints

### Health Check
```
GET /
```
Returns API status and information.

### Get All Products
```
GET /api/products
```
Fetches all products from Printful catalog.

### Get Specific Product
```
GET /api/products/{product_id}
```
Fetches details for a specific product by ID.

## Deployment to Render.com

### 1. Create New Web Service
1. Go to [Render.com](https://render.com) dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select the `Galactic-Archives/api-for-store` repository

### 2. Configure Service
- **Name**: `api-for-store` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Free tier is sufficient for development

### 3. Set Environment Variables
In Render.com dashboard, add the following environment variable:
- **Key**: `PRINTFUL_API_KEY`
- **Value**: Your Printful API key

### 4. Deploy
Click "Create Web Service" and wait for deployment to complete.

### 5. Get Your API URL
After deployment, Render will provide a URL like:
```
https://api-for-store-xxxx.onrender.com
```
Save this URL - you'll need it for the frontend configuration.

## Frontend Integration

Update the `store.html` file in the `admiral-Gal-Arch.io` repository to use your deployed API:

```javascript
// Replace this line:
const API_BASE = 'https://api.printful.com';

// With your Render URL:
const API_BASE = 'https://api-for-store-xxxx.onrender.com';

// Update API calls to use new endpoints:
fetch(`${API_BASE}/api/products`)  // Instead of ${API_BASE}/products
```

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository:
```bash
git clone https://github.com/Galactic-Archives/api-for-store.git
cd api-for-store
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
PRINTFUL_API_KEY=your_printful_api_key_here
```

4. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI web server
- **httpx**: Async HTTP client
- **python-dotenv**: Environment variable management

## Security Notes

- ✅ API keys are never committed to the repository
- ✅ API keys are stored as environment variables
- ✅ CORS is configured to only allow specific origins
- ✅ All API calls go through the backend proxy
- ⚠️ Remember to set `PRINTFUL_API_KEY` in Render.com environment variables

## License

This project is part of the Galactic Archives organization.
