# Railway Deployment Guide

## Step 1 — Add PostgreSQL on Railway
In your Railway project → click "+ New" → Database → PostgreSQL
Once created, click the Postgres service → Variables tab → copy the DATABASE_URL

## Step 2 — Environment Variables (set in Railway Dashboard → Variables tab)

GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
SECRET_KEY=s7f2kLmN9pQrXvYzA4bCdEgHiJoTuWx1
DATABASE_URL=<paste the PostgreSQL URL from Railway here>

## Step 3 — After first deploy
1. Copy your Railway app URL (e.g. https://planner-xyz.up.railway.app)
2. Go to Google Cloud Console → APIs & Services → Credentials → your OAuth client
3. Add to Authorized redirect URIs:
   https://planner-xyz.up.railway.app/api/auth/callback
4. Go to OAuth consent screen → Test users → + Add users → add all 4 emails

## Allowed login emails
- mdsajid2152@gmail.com
- awadtheman2@gmail.com
- khatoonkhamira23@gmail.com
- mdsajid84388@gmail.com
