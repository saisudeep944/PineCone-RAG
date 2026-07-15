# 🚀 Streamlit Frontend - Quick Start Guide

## What Changed?

We've replaced the React frontend with a beautiful, fully-featured **Streamlit-based frontend** that maintains all the advanced RAG capabilities:

✅ Real-time token streaming
✅ NDJSON protocol support  
✅ Source document retrieval
✅ Session management
✅ Document upload
✅ Dark mode UI
✅ Professional styling

## Installation

### Step 1: Install Dependencies

From the workspace root:

```bash
cd e:\Programs of Diff Languages\Pinecone_RAG
pip install -r frontend/requirements.txt
```

### Step 2: Start Backend

Ensure your FastAPI backend is running:

```bash
python main.py
# Should see: "Uvicorn running on http://127.0.0.1:8000"
```

### Step 3: Start Frontend

From the workspace root:

```bash
streamlit run frontend/app.py
```

The app opens automatically at: **http://localhost:8501**

## What's New in the UI?

### Sidebar (Left)
- 🤖 **Enterprise RAG** - Branded header
- 📁 **Namespace Selection** - Choose knowledge base
- ➕ **New Chat** - Start fresh conversation
- 🔄 **Clear Chat** - Reset messages
- 💬 **Recent Sessions** - Quick load previous chats
- ℹ️ **Tips** - Usage guidelines

### Main Chat Area
- 💬 **AI Chat Assistant** - Professional header
- 📝 **Chat History** - All messages preserved
- 📚 **Sources Panel** - View retrieved documents (expandable)
- 💬 **Chat Input** - Ask questions
- 📊 **Footer Stats** - Active namespace, message count, time

### Additional Pages
- 📤 **Upload** - Add documents to knowledge base
- 💬 **Sessions** - Manage all chat sessions

## Key Features

### 1. Real-time Streaming
When you send a message:
1. User message appears immediately
2. AI starts typing token by token
3. Sources show after response completes
4. Full context preserved in session

### 2. Namespace Organization
- Each namespace = separate knowledge base
- Switch namespaces in sidebar
- Upload documents to specific namespace
- Sessions tied to namespace

### 3. Source Attribution
After each response:
- Click "📚 View Sources" to expand
- See filename, chunk index, reranking score
- Read text preview from actual document
- Verify AI's knowledge base

### 4. Session Persistence
- Each chat creates a new session
- Sessions shown in sidebar
- Click to load previous conversation
- Message history maintained

## File Structure

```
frontend/
├── app.py                  ← Start here! Main chat interface
├── pages/
│   ├── upload.py          ← Upload documents
│   └── sessions.py        ← Manage sessions
├── services/
│   └── api_client.py      ← Backend communication
├── utils/
│   └── session_state.py   ← State management
├── styles/
│   └── custom.css         ← Beautiful dark theme
├── .streamlit/
│   └── config.toml        ← Streamlit config
├── requirements.txt       ← Dependencies
└── README.md             ← Full documentation
```

## Common Tasks

### 📤 Upload a Document

1. Click **Upload** in sidebar (if using multi-page)
2. OR go directly to: http://localhost:8501/upload
3. Select namespace
4. Choose file (PDF, CSV, TXT, DOCX)
5. Click "🚀 Upload Document"
6. Wait for processing
7. Use in chat immediately

### 💬 Start New Chat

1. Click **➕ New Chat** in sidebar
2. Or select namespace and it auto-creates
3. Type question in input
4. See real-time token streaming
5. Expand **📚 View Sources** to see where AI found info

### 📂 Load Previous Session

1. Look at **Recent Sessions** in sidebar
2. Click the **📂** button next to session
3. Chat history loads
4. Continue conversation

## API Connection

The frontend talks to your backend via REST API:

```
POST http://localhost:8000/chat/stream      ← Streaming responses
POST http://localhost:8000/session/create   ← New sessions
GET  http://localhost:8000/sessions         ← List sessions
GET  http://localhost:8000/namespaces       ← Available namespaces
POST http://localhost:8000/upload           ← Document upload
```

**If backend is on different host/port:**
Edit `frontend/services/api_client.py`:
```python
BASE_URL = "http://your-server:8000"
```

## Troubleshooting

### 🔴 "Connection Error"
```
✓ Ensure backend running: python main.py
✓ Check URL in api_client.py matches
✓ Verify firewall allows localhost:8000
```

### 🔴 "No namespaces available"
```
✓ Backend /namespaces endpoint working?
✓ Check backend logs for errors
✓ Verify Pinecone client configured
```

### 🔴 "Streaming stops mid-response"
```
✓ Check backend streaming not timing out
✓ Verify NDJSON format correct
✓ See backend logs for token generation
```

### 🔴 "CSS not loading"
```
✓ Check styles/custom.css exists
✓ Verify file permissions readable
✓ Clear browser cache: Ctrl+Shift+Delete
✓ Refresh Streamlit: Ctrl+R in app
```

## Performance Tips

1. **First Load Slow?**
   - Streamlit compilation takes 5-10 seconds first time
   - Subsequent runs are instant

2. **Streaming Choppy?**
   - Check network latency to backend
   - Verify backend not CPU-bound
   - Consider increasing token batch size

3. **UI Responsive?**
   - Streamlit reruns on every interaction
   - Use session state to cache expensive operations
   - Avoid large dataframes in sidebar

## Next Steps

1. **✅ Run the app**: `streamlit run frontend/app.py`
2. **✅ Ask a question**: Type in chat input
3. **✅ View sources**: Click "📚 View Sources"
4. **✅ Upload documents**: Use Upload page
5. **✅ Manage sessions**: View all chats in Sessions page

## Documentation

- **Full README**: See `frontend/README.md` for comprehensive docs
- **Backend API**: See `app/api/main.py` for endpoint specs
- **Streamlit Docs**: https://docs.streamlit.io/

## Questions?

Check:
1. Backend logs: `python main.py` output
2. Frontend logs: Streamlit console output
3. Browser console: F12 > Console tab
4. Network tab: F12 > Network tab (check API calls)

---

**Happy chatting! 🚀**
