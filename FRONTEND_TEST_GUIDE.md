# Quick Test Guide - Frontend Fixes

## Before You Start
1. Stop any running Streamlit processes
2. Make sure your backend (uvicorn) is still running on `http://localhost:8000`
3. Clear Streamlit cache (optional):
   ```bash
   rm -r ~/.streamlit  # Linux/Mac
   rmdir %USERPROFILE%\.streamlit  # Windows
   ```

## Start the Frontend
```bash
cd frontend
streamlit run app.py
```

The app should open at `http://localhost:8501`

---

## Issue Verification Tests

### Test 1: Chat Streaming (Empty Avatar Fix) ✓
**What was broken**: Empty bot avatar appeared, then message after delay

**How to test**:
1. Type a question in the chat box: "What are the top 3 features?"
2. **Observe**: Bot avatar should appear WITH content streaming in real-time
3. **Verify**: No empty avatar; smooth streaming with cursor indicator
4. **Result**: ✓ FIXED - Message appears immediately with content

---

### Test 2: Message Formatting (Markdown) ✓
**What was broken**: Messages show as plain text with # symbols, no formatting

**How to test**:
1. Ask a question that triggers a formatted response: "List the main points"
2. **Observe**: Response should show:
   - Bullet points (•) properly formatted
   - Headers with proper sizing (no # symbols)
   - Line breaks between sections
   - Bold text if present
3. **Result**: ✓ FIXED - Markdown renders correctly

---

### Test 3: Namespace Switching ✓
**What was broken**: Selecting new namespace didn't load its documents; chat showed nothing

**How to test**:
1. Look at sidebar "📁 Namespace" dropdown
2. Select a different namespace (if you have multiple with documents)
3. **Verify**: 
   - Green success message: "Switched to [namespace]"
   - Chat area clears
   - New session created
4. Ask a question - should answer from NEW namespace docs
5. Switch back - old namespace documents should work again
6. **Result**: ✓ FIXED - Proper namespace isolation

---

### Test 4: Streamlit Errors ✓
**What was broken**: 
- "st.switch_page(...)" error in Sessions page
- "border parameter" error in Recent Sessions

**How to test**:
1. Go to "Sessions" page (sidebar)
2. **Verify**: No error messages about `switch_page`
3. Recent Sessions showing 5 sessions in sidebar
4. **Verify**: No error about `border` parameter
5. Click a session load button
6. **Verify**: Redirects to main chat smoothly
7. **Result**: ✓ FIXED - No Streamlit API errors

---

### Test 5: Session Management ✓
**What was broken**: Session loading errors

**How to test**:
1. Create a session: Click "➕ New Chat"
2. Send a message: "Hello"
3. Click "📂" button next to a session in sidebar
4. **Verify**: 
   - Session loads successfully
   - Previous message appears in chat
   - No errors in console
5. **Result**: ✓ FIXED - Sessions work properly

---

### Test 6: Sources Display ✓
**What was broken**: Sources might not display properly

**How to test**:
1. Ask a question: "What products do you offer?"
2. Look for "📚 View Sources" expander
3. Click to expand
4. **Verify**:
   - Source file name shows
   - Chunk number and score display
   - Preview text is readable
5. **Result**: ✓ FIXED - Sources display correctly

---

## Expected Behavior After Fixes

| Feature | Before | After |
|---------|--------|-------|
| Chat Avatar | Empty, then filled | Appears with content |
| Streaming | Slow, with reruns | Smooth, real-time |
| Markdown | Plain text, # symbols | Properly formatted |
| Namespace Switch | No effect | New session, clears chat |
| Session Load | Error | Smooth redirect |
| Recent Sessions | Border error | Displays cleanly |
| Message Formatting | Broken | Headers, bullets work |

---

## Browser Console Troubleshooting

Open Browser DevTools (F12) and check **Console** tab for errors:

**Should NOT see**:
- ❌ `switch_page is not defined`
- ❌ `border parameter error`
- ❌ `streaming error`

**Should see**:
- ✅ WebSocket connection to backend
- ✅ Chat messages being sent/received
- ✅ No red error messages

---

## If Something Still Doesn't Work

### Common Issues:

**1. Backend not responding**
```bash
# Check if backend is running
curl http://localhost:8000/namespaces
# Should return JSON list of namespaces
```

**2. Old cache causing issues**
```bash
# Clear all Streamlit cache
streamlit cache clear
```

**3. Port conflicts**
```bash
# Find what's using port 8501
# Windows:
netstat -ano | findstr :8501
# Kill process and restart
```

**4. Module errors**
```bash
# Reinstall dependencies
pip install -r frontend/requirements.txt
```

---

## Success Indicators

All of these should work without errors:
- ✅ Send chat message → immediate bot response
- ✅ Switch namespaces → automatic session update
- ✅ Load session → redirect to chat with history
- ✅ View sources → expander shows metadata
- ✅ No console errors → clean logs
- ✅ Recent sessions display → no border errors

---

## Need Help?

Check the generated `FRONTEND_FIXES.md` for detailed technical information about each fix.

All changes are documented with line numbers and before/after code samples.
