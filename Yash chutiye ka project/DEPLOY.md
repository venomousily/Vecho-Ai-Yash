# Deploying Vecho Ai to Vercel

## Prerequisites

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Make sure you have a Vercel account (sign up at https://vercel.com)

## Deployment Steps

### Option 1: Using Vercel CLI

1. **Login to Vercel:**
   ```bash
   vercel login
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **For production deployment:**
   ```bash
   vercel --prod
   ```

### Option 2: Using Vercel Dashboard

1. Go to https://vercel.com/new
2. Import your Git repository (GitHub, GitLab, or Bitbucket)
3. Vercel will automatically detect the configuration
4. Click "Deploy"

## Important Notes

### Database Storage
⚠️ **Important**: Vercel serverless functions use `/tmp` directory which is **ephemeral**. 
- Data will be lost when the function goes to sleep
- For production, consider using:
  - **Vercel Postgres** (recommended)
  - **Supabase** (free tier available)
  - **PlanetScale** (MySQL)
  - **MongoDB Atlas** (free tier)

### Environment Variables
If you need to change the Gemini API key, add it as an environment variable in Vercel:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add: `GEMINI_API_KEY` with your API key value

Then update `backend/gemini_client.py` to use:
```python
API_KEY = os.getenv('GEMINI_API_KEY', 'your-default-key')
```

### File Structure
The project structure for Vercel:
```
.
├── api/
│   └── index.py          # Serverless function entry point
├── backend/
│   ├── app.py
│   └── gemini_client.py
├── frontend/
│   └── index.html
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── vecho ai logo.png
```

## Troubleshooting

### Database Issues
If you see database errors, the `/tmp` directory might not be writable. Consider migrating to a cloud database.

### API Routes Not Working
- Check that `vercel.json` routes are configured correctly
- Ensure all API routes start with `/api/`

### Static Files Not Loading
- Make sure files are in the `frontend/` directory
- Check that routes in `vercel.json` are correct

## Post-Deployment

After deployment, your app will be available at:
- Preview: `https://your-project-name.vercel.app`
- Production: `https://your-project-name.vercel.app` (or custom domain)

## Next Steps

1. **Set up a persistent database** (recommended for production)
2. **Add environment variables** for API keys
3. **Configure custom domain** (optional)
4. **Set up monitoring** in Vercel dashboard

