# AgriGPT – Step-by-Step Render Deployment

Deploy backend and frontend on Render. In-memory chat (no Redis).

---

## Part 1: Backend (API)

### Step 1: Open Render

1. Go to [render.com](https://render.com)
2. Sign in (or sign up with GitHub)
3. Click **Dashboard**

### Step 2: Create Backend Service

1. Click **New +**
2. Select **Web Service**

### Step 3: Connect Repository

1. If not connected: **Connect account** → choose **GitHub** → authorize
2. Find **AgriGPT** and click **Connect**

### Step 4: Backend Settings

| Field | Value |
|-------|-------|
| **Name** | `agrigpt-api` |
| **Region** | Oregon (US West) or nearest |
| **Branch** | `main` |

### Step 5: Runtime – Docker

1. Set **Runtime** to **Docker**
2. **Root Directory:** leave blank
3. **Dockerfile Path:** leave blank (uses `Dockerfile` at repo root)

### Step 6: Instance Type

1. Choose **Free**
2. Free tier: 750 hrs/month, sleeps after 15 min idle

### Step 7: Environment Variables

Click **Advanced** → **Add Environment Variable** and add:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | Your Groq API key (from console.groq.com) |

Optional:

| Key | Value |
|-----|-------|
| `OPENWEATHER_API_KEY` | Your OpenWeather key (for weather in header) |

### Step 8: Deploy Backend

1. Click **Create Web Service**
2. Wait for build and deploy (about 5–10 min)
3. When done, the service URL appears (e.g. `https://agrigpt-api.onrender.com`)
4. Copy this URL – you need it for the frontend

### Step 9: Test Backend

```bash
curl https://YOUR-BACKEND-URL.onrender.com/health
```

Example response:

```json
{
  "status": "OK",
  "service": "AgriGPT Backend",
  ...
}
```

---

## Part 2: Frontend

### Step 10: Create Frontend Service

1. In the Dashboard, click **New +**
2. Select **Static Site**

### Step 11: Connect Same Repo

1. Select the **AgriGPT** repository
2. Click **Connect**

### Step 12: Frontend Settings

| Field | Value |
|-------|-------|
| **Name** | `agrigpt` |
| **Branch** | `main` |
| **Root Directory** | `frontend-main` |

### Step 13: Build & Publish

| Field | Value |
|-------|-------|
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `dist` |

### Step 14: Environment Variable (Important)

1. Expand **Environment** / **Environment Variables**
2. Add:

| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | `https://YOUR-BACKEND-URL.onrender.com` |

Replace `YOUR-BACKEND-URL` with the backend URL from Step 8 (e.g. `agrigpt-api`).

Examples:
- `https://agrigpt-api.onrender.com`
- No trailing slash.

### Step 15: Deploy Frontend

1. Click **Create Static Site**
2. Wait for build (about 2–3 min)
3. Note the frontend URL (e.g. `https://agrigpt.onrender.com`)

### Step 16: Test Frontend

1. Open the frontend URL in a browser
2. Try a text query (e.g. “What fertilizer for wheat?”)
3. If the backend was asleep, the first request may take ~1 minute; later ones should be fast

---

## Summary

| Service | Type | URL |
|---------|------|-----|
| Backend | Web Service (Docker) | `https://agrigpt-api.onrender.com` |
| Frontend | Static Site | `https://agrigpt.onrender.com` |

**Free limits:** Backend sleeps after 15 min; first request after that ~1 min to wake. Frontend does not sleep.
