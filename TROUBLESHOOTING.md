# ⚡ Quick Troubleshooting Guide

## Common Issues & Solutions

### Issue 1: Routes Not Found (404 Error)
**Symptom**: `/interview-practice`, `/interview-feedback`, `/interview-roadmap` return 404

**Solution**:
1. Verify routes are in `app/routes.py` (Lines 3230-3252)
2. Check Flask app is restarted (old process might be cached)
3. Ensure imports are correct at top of routes.py
4. Restart Flask: `python run.py`

### Issue 2: Templates Not Rendering
**Symptom**: Page shows but layout is broken or CSS not loading

**Solution**:
1. Check files exist in `app/templates/`:
   - `interview-practice.html` ✓
   - `interview-feedback.html` ✓
   - `interview-roadmap.html` ✓
2. Verify paths in `<link>` tags use `{{ url_for() }}` correctly
3. Clear browser cache: Ctrl+Shift+Delete
4. Check Flask server logs for render errors

### Issue 3: CSS Not Applying
**Symptom**: Pages load but styling looks wrong

**Solution**:
1. Verify `placement.css` is linked: `<link rel="stylesheet" href="{{ url_for('static', filename='css/placement.css') }}">`
2. CSS file exists: `app/static/css/placement.css` ✓
3. Check for CSS class conflicts with Spline viewer
4. Inspect element (F12) to see actual CSS being applied
5. Clear browser cache

### Issue 4: JavaScript Errors (Console)
**Symptom**: Open browser console (F12) and see JavaScript errors

**Solution**:
1. Check if session_id is in URL: `?session_id=xxxxx`
2. Verify API endpoints being called exist
3. Check fetch requests in Network tab (F12 → Network)
4. Ensure user is logged in before accessing pages
5. Look for CORS errors if APIs on different domain

### Issue 5: API Returns 401 Unauthorized
**Symptom**: API calls fail with 401 error

**Solution**:
1. Verify user session is active: Check `session.get("user_email")`
2. Login first before accessing interview pages
3. Check cookies are set correctly
4. Ensure CORS headers are correct if cross-domain

### Issue 6: No Questions Loaded
**Symptom**: Interview practice page shows but no questions appear

**Solution**:
1. Verify `/api/placement/questions/generate` API endpoint exists
2. Check if questions exist in database for this session
3. Verify session_id is valid and belongs to current user
4. Test API in Postman: `GET /api/placement/questions/generate?session_id=123`
5. Check API returns JSON in expected format

### Issue 7: Progress Not Saving
**Symptom**: Checkboxes on roadmap page don't persist after refresh

**Solution**:
1. Verify `/api/placement/roadmap/{id}/progress` PUT endpoint exists
2. Check browser console for fetch errors
3. Ensure user_id is correctly associated with roadmap
4. Check database has progress_tracking table
5. Test API with Postman

### Issue 8: Mobile Layout Broken
**Symptom**: Page looks bad on phone/small screen

**Solution**:
1. Check media query at 768px in CSS
2. Verify grid-template-columns uses `repeat(auto-fit, ...)`
3. Test in browser DevTools: Ctrl+Shift+M (mobile view)
4. Check button width is 100% on mobile
5. Verify font sizes don't overflow

---

## Testing Checklist

### Basic Setup (Before Testing)
- [ ] Requirements installed: `pip install -r requirements.txt`
- [ ] Flask app starts: `python run.py`
- [ ] App accessible: `http://localhost:5000`
- [ ] User can login
- [ ] Dashboard loads with "Interview Prep" card

### Route Testing
- [ ] Can visit `/interview-practice?session_id=test` (should show 200)
- [ ] Can visit `/interview-feedback?session_id=test` (should show 200)
- [ ] Can visit `/interview-roadmap?session_id=test` (should show 200)
- [ ] All routes redirect to login if not authenticated

### UI Testing
- [ ] Interview Practice page:
  - [ ] Questions display
  - [ ] Timer counts up
  - [ ] Character counter updates
  - [ ] Submit button saves answer
  - [ ] Skip button moves to next question
- [ ] Interview Feedback page:
  - [ ] Overall score displays
  - [ ] 4 dimension scores show
  - [ ] Strengths list populates
  - [ ] Weaknesses list populates
  - [ ] Model answer displays
- [ ] Interview Roadmap page:
  - [ ] Timeline shows all 21 days
  - [ ] Checkboxes work
  - [ ] Download button creates CSV
  - [ ] Resource links work

### API Testing (With Postman or curl)
```bash
# Test questions endpoint
curl -X GET "http://localhost:5000/api/placement/questions/generate?session_id=1" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test answer submission
curl -X POST "http://localhost:5000/api/placement/answers/submit" \
  -H "Content-Type: application/json" \
  -d '{"session_id": 1, "question_id": 1, "answer": "test", "time_taken": 60}'

# Test results endpoint
curl -X GET "http://localhost:5000/api/placement/session/1/results" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test roadmap endpoint
curl -X GET "http://localhost:5000/api/placement/roadmap/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Mobile Testing
1. Open DevTools: F12
2. Toggle device toolbar: Ctrl+Shift+M
3. Select iPhone 12 (390x844)
4. Test each page:
   - [ ] Buttons are full width
   - [ ] Grid items stack vertically
   - [ ] Text is readable
   - [ ] No horizontal scroll
5. Test on real phone if possible (use `http://YOUR_IP:5000`)

---

## Performance Optimization Tips

### If Pages Load Slowly
1. **Check API response time**:
   - Open DevTools → Network tab
   - See how long `/api/placement/questions/generate` takes
   - If > 2s, optimize API backend
2. **Minify CSS**: Remove comments from placement.css
3. **Lazy load resources**: Don't load all 21 days at once
4. **Cache questions**: Client-side storage

### If Roadmap Regenerate is Slow
1. Roadmap generation might be intensive
2. Add loading indicator while regenerating
3. Consider async processing on backend
4. Show progress bar during generation

---

## Browser Console Debugging

Open F12 and run these to debug:

```javascript
// Check if session_id is loaded
const urlParams = new URLSearchParams(window.location.search);
console.log("Session ID:", urlParams.get('session_id'));

// Check API response
fetch('/api/placement/questions/generate?session_id=1')
  .then(r => r.json())
  .then(d => console.log("Questions:", d));

// Check local storage
console.log("LocalStorage:", localStorage);

// Check current user session
fetch('/api/user/profile')
  .then(r => r.json())
  .then(d => console.log("User:", d));
```

---

## Files to Check If Issues Persist

Priority order for debugging:

1. **Flask App Init** (`app/__init__.py`)
   - Line 37: `from .routes import main` should load without errors

2. **Routes File** (`app/routes.py`)
   - Lines 3230-3252: New routes should be there
   - Check no syntax errors in file

3. **Templates** (`app/templates/`)
   - `interview-practice.html` - Check syntax, no missing closing tags
   - `interview-feedback.html` - Check syntax
   - `interview-roadmap.html` - Check syntax

4. **CSS** (`app/static/css/placement.css`)
   - Check for syntax errors
   - Verify colors are correct hex values
   - Check media queries are valid

5. **JavaScript Console** (Browser F12)
   - Check for JavaScript errors
   - Check Network tab for failed requests
   - Check CORS issues

---

## Quick Commands for Common Tasks

```bash
# Start Flask app
python run.py

# Kill Flask app
# In terminal: Ctrl+C

# Check Python syntax
python -m py_compile app/routes.py

# Check if routes are registered
python -c "from app import create_app; app = create_app(); routes = [str(r) for r in app.url_map.iter_rules()]; [print(r) for r in routes if 'interview' in r]"

# Install missing dependency
pip install package_name

# Clear browser cache
# Chrome/Edge: Ctrl+Shift+Delete
# Firefox: Ctrl+Shift+Delete
```

---

## Getting Help

If stuck, check:
1. **File contents**: Verify files weren't corrupted
2. **File paths**: Use absolute paths if relative paths fail
3. **Permissions**: Make sure files are readable
4. **Encoding**: Files should be UTF-8 encoded
5. **Line endings**: Should be consistent (LF for Linux, CRLF for Windows)

Look for `INTERVIEW_UI_INTEGRATION.md` for complete integration documentation.
