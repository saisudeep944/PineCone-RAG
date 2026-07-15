# Enterprise RAG Frontend - Streamlit Edition

Beautiful, modern Streamlit-based frontend for the Enterprise RAG system. Features real-time token streaming, source retrieval, namespace management, and document upload capabilities.

## Architecture

```
frontend/
├── app.py                  # Main chat interface (entry point)
├── pages/
│   ├── chat.py            # (Integrated into app.py)
│   ├── sessions.py        # Session manager & history
│   └── upload.py          # Document upload interface
├── services/
│   └── api_client.py      # Backend API communication layer
├── utils/
│   └── session_state.py   # Streamlit session state management
└── styles/
    └── custom.css         # Beautiful dark theme styling
```

## Features

### 🎯 Main Chat Interface (`app.py`)
- **Real-time Token Streaming**: NDJSON protocol for smooth token delivery
- **Namespace Management**: Organize conversations by knowledge base
- **Session Management**: Create, view, and load chat sessions
- **Smart Sources Panel**: View retrieved document chunks with reranking scores
- **Auto Session Creation**: Automatic session generation for new conversations
- **Message History**: Persistent conversation tracking per session

### 📁 Document Management (`pages/upload.py`)
- **Multi-format Support**: PDF, CSV, TXT, DOCX
- **Namespace Organization**: Upload to specific knowledge bases
- **Status Feedback**: Real-time upload progress
- **Immediate Indexing**: Documents available for queries right after upload

### 💬 Session Management (`pages/sessions.py`)
- **Session Listing**: View all active sessions
- **Quick Load**: Switch between sessions instantly
- **Metadata Display**: See namespace, message count, creation time

## Setup & Installation

### Prerequisites
- Python 3.9+
- Streamlit
- Backend server running on `http://localhost:8000`

### Installation

1. **Install Streamlit**
```bash
pip install streamlit
```

2. **Configure Backend URL** (if not localhost)
Edit `services/api_client.py`:
```python
BASE_URL = "http://your-backend-url:8000"
```

### Running the App

```bash
# From the workspace root (e:\Programs of Diff Languages\Pinecone_RAG\)
streamlit run frontend/app.py
```

The app will open at: `http://localhost:8501`

## API Integration

### Backend Requirements

The Streamlit frontend expects these FastAPI endpoints:

#### Chat Streaming
```
POST /chat/stream
Body: {"session_id": "...", "message": "..."}
Response: NDJSON stream with events:
  - {"type": "token", "content": "word_or_whitespace"}
  - {"type": "metadata", "status": "...", "sources": [...]}
  - {"type": "complete"}
```

#### Session Management
```
POST /session/create
Body: {"namespace": "..."}
Response: {"session_id": "..."}

GET /sessions
Response: {"sessions": [...]}
```

#### Namespaces
```
GET /namespaces
Response: {"namespaces": [...]}
```

#### Document Upload
```
POST /upload
Form: {file, namespace}
Response: JSON response
```

## Streaming Protocol

The frontend expects NDJSON (newline-delimited JSON) responses from `/chat/stream`:

```json
{"type": "token", "content": "Hello"}
{"type": "token", "content": " "}
{"type": "token", "content": "world"}
{"type": "metadata", "status": "success", "intent": "query", "sources": [...]}
{"type": "complete"}
```

**Event Types:**
- `token`: Individual token/text chunk for real-time display
- `metadata`: Response metadata (status, intent, source documents)
- `complete`: Signals end of stream

## UI Components

### Sidebar
- **Namespace Selection**: Switch knowledge bases
- **New Chat**: Create fresh session
- **Clear Chat**: Reset message history
- **Session Browser**: Quick-load recent sessions
- **Tips**: Usage guidelines

### Main Chat Area
- **Message Display**: User and assistant messages with distinct styling
- **Sources Panel**: Expandable section showing:
  - Document filename
  - Chunk index
  - Reranking score
  - Text preview
- **Chat Input**: Responsive input field with autocomplete suggestions
- **Footer**: Session stats and metadata

## Styling

### Theme
- **Dark Mode**: Eye-friendly dark background (`#0a0d12`)
- **Accent Color**: Professional blue (`#1e3a8a` → `#3b82f6`)
- **Contrast**: High contrast white text for readability

### Key CSS Classes
- `.sidebar-header`: Branded header with gradient
- `.main-header`: Main chat area header
- `.source-card`: Document source styling
- `.sidebar-footer`: Help and tips section

### Customization
Edit `styles/custom.css` to modify:
- Colors: Update CSS variables in `:root`
- Fonts: Change `font-family` in `html, body`
- Spacing: Adjust padding/margins
- Border radius: Modify `border-radius` values

## Session State Management

Located in `utils/session_state.py`:

```python
initialize_session_state()  # Init all state variables
add_message(role, content)  # Add to conversation
get_messages()              # Retrieve all messages
set_session_id(id)          # Update session
set_namespace(namespace)    # Update namespace
```

## NDJSON Parser

The app's streaming parser (in `app.py`):

```python
for line in stream_chat(session_id, prompt):
    if line.strip():
        event = json.loads(line)
        
        if event.get("type") == "token":
            full_response += event.get("content", "")
            response_container.markdown(full_response)
        
        elif event.get("type") == "metadata":
            response_metadata = event
```

Handles:
- Whitespace preservation
- Real-time token accumulation
- Metadata extraction
- Error handling with `JSONDecodeError`

## Troubleshooting

### "Error loading namespaces"
- Check backend running on correct URL
- Verify `/namespaces` endpoint responding

### "Stream connection failed"
- Ensure `/chat/stream` returns NDJSON
- Check CORS settings in FastAPI backend
- Verify `session_id` format

### Messages not appearing
- Check browser console for errors
- Verify `st.session_state.messages` populated
- Confirm markdown rendering enabled

### Styling not applied
- Verify `styles/custom.css` path correct
- Check CSS syntax (missing semicolons)
- Clear browser cache and reload

## Performance Tips

1. **Streaming Optimization**
   - Keep tokens small (50-100 chars) for smooth display
   - Use `response_container.markdown()` for real-time updates

2. **Session Management**
   - Limit recent sessions shown to 5-10
   - Cache namespace list for quick selection

3. **CSS Loading**
   - Minify custom.css in production
   - Use CSS variables for theme consistency

## Future Enhancements

- [ ] Multi-language support
- [ ] Export chat as PDF
- [ ] Custom prompt templates
- [ ] Advanced search filters
- [ ] User authentication
- [ ] Chat analytics dashboard
- [ ] Dark/Light theme toggle
- [ ] Conversation export (JSON, Markdown)

## Dependencies

```
streamlit>=1.28.0
requests>=2.31.0
pandas>=2.0.0
```

Install with:
```bash
pip install streamlit requests pandas
```

## Support

For issues or questions:
1. Check backend logs for API errors
2. Review browser console for JavaScript errors
3. Verify file permissions in upload directory
4. Check Streamlit documentation: https://docs.streamlit.io
