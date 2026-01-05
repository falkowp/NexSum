# NexSum Frontend

React + Vite frontend for NexSum (text summarization UI).

Quick start:

```powershell
cd frontend
npm install
npm run dev
```

To run backend locally from the frontend folder:

```powershell
npm run start-api
```

Notes:
- Backend API base URL: http://127.0.0.1:5000 (endpoints under `/api/`)
- Ensure backend is running before using upload/transcribe features
- Use `npm run dev-all` to start frontend and backend concurrently

```json
// Example: start-api script in package.json
"start-api": "python ../backend/app.py"
```

Contributions: Please open issues/PRs and follow project `CONTRIBUTING.md` if present.
