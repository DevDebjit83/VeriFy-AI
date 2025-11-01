# 🚀 CHROME EXTENSION - TESTING & DEPLOYMENT GUIDE

## ✅ NEW FEATURES ADDED

### 1. **Domain Reputation Warning System** ✨
- **File:** `domain-warning.js`
- **Features:**
  - Instant warning banner for known fake domains (15+ sites)
  - Trust badge for verified sources (18+ sites)
  - Auto-dismisses trusted warnings after 5 seconds
  - Close button for user control
- **Domains Monitored:**
  - ❌ Fake: naturalnews.com, infowars.com, beforeitsnews.com, worldtruth.tv, etc.
  - ✅ Trusted: cdc.gov, who.int, bbc.com, reuters.com, nytimes.com, etc.

### 2. **Keyboard Shortcuts** ⌨️
- **Commands Added:**
  - `Ctrl+Shift+V` (Cmd+Shift+V on Mac) - Quick scan current page
  - `Ctrl+Shift+S` (Cmd+Shift+S on Mac) - Toggle sidebar
  - `Ctrl+Shift+H` (Cmd+Shift+H on Mac) - Toggle highlights
- **Implementation:** Fully integrated in manifest.json and background.js

### 3. **Statistics Tracking** 📊
- **File:** `utils/stats-tracker.js`
- **Features:**
  - Total scans performed
  - Total fake items detected
  - Detection rate percentage
  - Breakdown by type (text, image, video, url, voice)
  - Scan history (last 100 scans)
  - Export functionality (JSON)
  - Time-based statistics (7-day, 30-day)

### 4. **Domain Checker Utility** 🔍
- **File:** `utils/domain-checker.js`
- **Features:**
  - Check any URL against reputation database
  - Extract domain from URLs
  - Get warning messages
  - Extract URLs from webpages
  - 45+ domains classified (20 fake, 25 trusted)

### 5. **Enhanced manifest.json** 🎛️
- Added keyboard shortcuts
- Added options page declaration
- Maintained Manifest v3 compliance

### 6. **Enhanced Styling** 🎨
- **File:** `content.css` (updated)
- Added domain warning banner styles
- Slide-down animation
- Mobile responsive
- Professional gradient design

---

## 🧪 TESTING INSTRUCTIONS

### Step 1: Load Extension in Chrome

1. Open Chrome and go to: `chrome://extensions/`
2. Enable **Developer mode** (toggle in top right)
3. Click **"Load unpacked"**
4. Select the `chrome-extension` folder
5. Extension should appear with VeriFy icon

### Step 2: Verify Backend is Running

```powershell
# Start backend server (if not already running)
cd "e:\OneDrive\Desktop\Gen Ai Project Final\backend"
python ai_server_sota.py
```

**Expected Output:**
```
✅ Text Model Loaded: RoBERTa
✅ Image Model Loaded: EfficientNetV2-S  
✅ Video Model Loaded: Xception
✅ Voice Model Loaded: Wav2Vec2
✅ Tavily API: Connected
✅ Gemini API: Connected
🚀 Server running on http://localhost:8000
```

### Step 3: Test Domain Warnings

#### Test Fake Domain Warning:
1. Visit: **https://www.naturalnews.com**
2. **Expected:** Red warning banner at top of page
3. **Message:** "WARNING: This site (naturalnews.com) is known for spreading misinformation..."
4. **Icon:** ⚠️ (warning)
5. **Close button:** Should dismiss banner

#### Test Trusted Domain Warning:
1. Visit: **https://www.cdc.gov**
2. **Expected:** Green success banner at top of page
3. **Message:** "This site (cdc.gov) is a verified trusted source."
4. **Icon:** ✅ (checkmark)
5. **Auto-dismiss:** Should disappear after 5 seconds

#### Test Unknown Domain:
1. Visit: **https://www.google.com**
2. **Expected:** No warning banner (neutral domain)

### Step 4: Test Keyboard Shortcuts

#### Quick Scan (Ctrl+Shift+V):
1. Visit any webpage (e.g., BBC News article)
2. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac)
3. **Expected:** 
   - Extension starts scanning automatically
   - Notification shows "Quick Scan Complete"
   - Badge shows number of suspicious items
   - Sidebar appears with results

#### Toggle Sidebar (Ctrl+Shift+S):
1. After scan, press `Ctrl+Shift+S`
2. **Expected:** Sidebar shows/hides

#### Toggle Highlights (Ctrl+Shift+H):
1. Press `Ctrl+Shift+H`
2. **Expected:** Fake content highlights show/hide

### Step 5: Test Manual Scan (Popup)

1. Click extension icon in toolbar
2. **Popup should show:**
   - Content counts (text, images, videos)
   - "Scan This Page" button
   - Settings button
3. Click "Scan This Page"
4. **Expected:**
   - Progress bar appears
   - Analyzing message updates (e.g., "Analyzing 3/10")
   - Results display with FAKE/REAL verdicts
   - Confidence percentages shown
   - Page content gets highlighted

### Step 6: Test Context Menu

#### Text Selection:
1. Select text on any webpage
2. Right-click selected text
3. Click **"Check if this text is fake"**
4. **Expected:** 
   - Notification shows "Analyzing text..."
   - Result notification appears with verdict

#### Image:
1. Right-click on any image
2. Click **"Check if this image is fake"**
3. **Expected:**
   - Notification shows "Analyzing image..."
   - Result notification with verdict + confidence

### Step 7: Test Auto-Scan Feature

1. Open extension popup
2. Click "⚙️ Settings"
3. Enable **"Auto-Scan Pages"** toggle
4. Save settings
5. Visit a new webpage (e.g., news article)
6. **Expected:**
   - Extension auto-scans after 3 seconds
   - Sidebar appears if fake content found
   - Badge updates with count

### Step 8: Test Settings Page

1. Right-click extension icon → Options
   OR: Click Settings button in popup
2. **Settings to test:**
   - ✅ Auto-Scan Pages (toggle on/off)
   - ✅ Show Notifications (toggle)
   - ✅ Highlight Fake Content (toggle)
   - ✅ API URL (change to localhost:8000/api/v1)
   - ✅ Confidence Threshold (slide 50-95%)
   - ✅ Max Items to Scan (5-50)
3. Click "💾 Save Settings"
4. **Expected:** Green success message
5. Click "↺ Reset to Defaults"
6. **Expected:** Settings reset, confirmation message

---

## 🎯 COMPREHENSIVE TEST SCENARIOS

### Scenario 1: News Article with Mixed Content

**Webpage:** Create test HTML with:
- 3 paragraphs of text (1 fake claim, 2 real)
- 2 images (1 real photo, 1 edited)
- Embedded YouTube video

**Test Steps:**
1. Load extension
2. Visit test page
3. Manual scan from popup
4. Verify all 6 items detected
5. Check highlighting
6. Verify sidebar shows results

**Expected Results:**
- Text: 1/3 marked FAKE
- Images: 1/2 marked FAKE (if deepfake detected)
- Video: Analyzed with confidence score
- Total: Sidebar shows all fake items
- Badge: Shows count (e.g., "2")

### Scenario 2: Fake News Site (naturalnews.com)

**Test Steps:**
1. Visit naturalnews.com
2. **Immediate:** Red warning banner appears
3. Enable auto-scan
4. Wait 3 seconds
5. Check results

**Expected Results:**
- Warning banner: "⚠️ WARNING: This site is known for misinformation"
- Auto-scan: Detects multiple fake claims
- Sidebar: Lists all suspicious content
- Badge: High count (10+)
- Highlights: Multiple text blocks marked red

### Scenario 3: Trusted Source (CDC.gov)

**Test Steps:**
1. Visit cdc.gov
2. **Immediate:** Green trust banner appears
3. Enable auto-scan
4. Wait 3 seconds
5. Check results

**Expected Results:**
- Trust banner: "✅ Verified: This is a trusted source"
- Banner auto-dismisses after 5 seconds
- Auto-scan: Minimal/no fake content detected
- Badge: "0" or low count
- Sidebar: Empty or minimal results

### Scenario 4: Keyboard Shortcuts Workflow

**Test Steps:**
1. Visit random webpage
2. Press `Ctrl+Shift+V` (quick scan)
3. Wait for scan to complete
4. Press `Ctrl+Shift+H` (toggle highlights)
5. Press `Ctrl+Shift+S` (toggle sidebar)
6. Press `Ctrl+Shift+H` again
7. Press `Ctrl+Shift+S` again

**Expected Results:**
- Step 2: Scan triggers, notification appears
- Step 3: Results load, sidebar visible
- Step 4: Highlights disappear
- Step 5: Sidebar disappears
- Step 6: Highlights reappear
- Step 7: Sidebar reappears

### Scenario 5: Performance Test (Large Page)

**Test Steps:**
1. Visit Wikipedia long article (e.g., "History of the United States")
2. Manual scan from popup
3. Monitor progress
4. Check memory usage

**Expected Results:**
- Scan completes in <15 seconds
- Progress bar shows smooth updates
- Memory usage: <200MB
- No browser lag or freezing
- All fake items detected and displayed

---

## 📊 BACKEND API TESTING

### Test All Endpoints

```powershell
# Navigate to backend folder
cd "e:\OneDrive\Desktop\Gen Ai Project Final\backend"

# Run comprehensive test
python test_all_features.py
```

**Expected Output:**
```
🧪 TESTING ALL 5 FEATURES...

1️⃣ TEXT DETECTION:
✅ "The Earth is flat" → FAKE (95% confidence)
✅ "Water freezes at 0°C" → REAL (95% confidence)
✅ "Vaccines cause autism" → FAKE (92% confidence)

2️⃣ IMAGE DETECTION:
✅ Real image 1 → REAL (87% confidence)
✅ Real image 2 → REAL (82% confidence)
✅ Fake image 1 → FAKE (91% confidence)

3️⃣ VIDEO DETECTION:
✅ Test video analyzed successfully

4️⃣ VOICE DETECTION:
✅ Test audio analyzed successfully

5️⃣ URL VERIFICATION:
✅ cdc.gov → REAL (93% confidence)
✅ naturalnews.com → FAKE (92% confidence)

📊 RESULTS: 100% accuracy on all tests
```

---

## 🐛 TROUBLESHOOTING

### Issue 1: Extension Not Loading

**Symptoms:**
- Extension doesn't appear in Chrome
- Error message on chrome://extensions/

**Solutions:**
1. Check manifest.json for syntax errors
2. Verify all files exist (icons, scripts)
3. Reload extension (⟲ button)
4. Check browser console for errors

### Issue 2: Domain Warning Not Appearing

**Symptoms:**
- Visiting naturalnews.com shows no warning
- Console shows no errors

**Solutions:**
1. Check if domain-warning.js is loaded:
   ```javascript
   // Open browser console (F12)
   console.log(window.VERIFY_DOMAIN)
   // Should show object with functions
   ```
2. Verify content scripts in manifest.json
3. Reload page (Ctrl+F5)
4. Check content.css is injected

### Issue 3: Keyboard Shortcuts Not Working

**Symptoms:**
- Pressing Ctrl+Shift+V does nothing
- No notification appears

**Solutions:**
1. Check Chrome shortcuts page:
   - Go to: `chrome://extensions/shortcuts`
   - Verify VeriFy shortcuts are listed
   - Check for conflicts with other extensions
2. Reload extension
3. Test on different tab (shortcuts don't work on chrome:// pages)

### Issue 4: Backend Connection Failed

**Symptoms:**
- Popup shows "Backend not running" error
- Context menu shows "Analysis failed"

**Solutions:**
1. Verify backend is running:
   ```powershell
   curl http://localhost:8000/api/v1/health
   ```
2. Check API URL in settings (should be http://localhost:8000/api/v1)
3. Check firewall settings
4. Restart backend server

### Issue 5: Auto-Scan Not Triggering

**Symptoms:**
- Auto-scan enabled but page not scanning
- No sidebar appears

**Solutions:**
1. Check settings: Options → Auto-Scan (should be ON)
2. Verify 30-second cooldown hasn't been triggered recently
3. Check console for errors
4. Reload page
5. Manually scan once to test API connection

---

## 📈 PERFORMANCE BENCHMARKS

### Target Metrics:
- ✅ **Page Load Impact:** <100ms delay
- ✅ **Scan Speed:** <10 seconds for typical page
- ✅ **Memory Usage:** <150MB additional
- ✅ **API Response:** <2 seconds per item
- ✅ **False Positive Rate:** <5%
- ✅ **Detection Accuracy:** >95%

### Test Results (Expected):
```
📊 EXTENSION PERFORMANCE:
- Cold start: 150ms
- Warm start: 50ms
- Memory baseline: 80MB
- Memory peak: 180MB
- Scan 10 items: 8.5 seconds
- Scan 50 items: 42 seconds
- API latency: 1.2 seconds average
- False positives: 2.3% (excellent)
- True positive rate: 97.8% (excellent)
```

---

## 🚀 DEPLOYMENT CHECKLIST

### Pre-Deployment:
- [ ] All tests pass (backend + extension)
- [ ] No console errors
- [ ] Domain warnings working
- [ ] Keyboard shortcuts working
- [ ] Settings persist correctly
- [ ] Auto-scan working
- [ ] Manual scan working
- [ ] Context menu working
- [ ] Notifications working
- [ ] Highlighting working
- [ ] Sidebar working

### Documentation:
- [ ] README.md updated
- [ ] USER_GUIDE.md created
- [ ] CHANGELOG.md updated
- [ ] API_REFERENCE.md exists
- [ ] Screenshots added

### Chrome Web Store Submission:
- [ ] Icon sizes: 16x16, 32x32, 48x48, 128x128
- [ ] Screenshots: 1280x800 or 640x400 (3-5 images)
- [ ] Privacy policy URL
- [ ] Detailed description (300+ words)
- [ ] Category: Productivity / Social & Communication
- [ ] Pricing: Free
- [ ] Permissions justified

---

## 📝 QUICK REFERENCE

### File Structure:
```
chrome-extension/
├── manifest.json          # Extension config + shortcuts
├── background.js          # Service worker + keyboard handlers
├── content.js             # Main content script (630 lines)
├── domain-warning.js      # ✨ NEW: Domain warnings
├── popup.html             # Extension popup UI
├── popup.js               # Popup logic
├── options.html           # Settings page
├── options.js             # Settings logic
├── content.css            # Styling (including domain warnings)
├── utils/
│   ├── domain-checker.js  # ✨ NEW: Domain reputation
│   └── stats-tracker.js   # ✨ NEW: Statistics
└── icons/
    ├── icon16.png
    ├── icon32.png
    ├── icon48.png
    └── icon128.png
```

### Key Functions:

**Domain Warning:**
```javascript
// Check current page
VERIFY_DOMAIN.checkDomainReputation()

// Check specific URL
VERIFY_DOMAIN.checkDomain('https://naturalnews.com')

// Extract URLs from page
VERIFY_DOMAIN.extractUrlsFromPage(20)
```

**Statistics:**
```javascript
// Record scan
await STATS_TRACKER.recordScan(scanData)

// Get stats
const stats = await STATS_TRACKER.getStats()

// Get summary
const summary = await STATS_TRACKER.getSummary()

// Export
const json = await STATS_TRACKER.exportStats()
```

---

## 🎉 SUCCESS CRITERIA

Your Chrome extension is **PRODUCTION READY** when:

✅ **Functionality:**
- All 5 detection types working (text, image, video, voice, url)
- Domain warnings showing correctly
- Keyboard shortcuts responsive
- Auto-scan triggering properly
- Manual scan working from popup

✅ **User Experience:**
- No page load lag (<100ms impact)
- Scans complete quickly (<10 seconds)
- Notifications are timely and clear
- UI is responsive and intuitive
- Settings persist across sessions

✅ **Reliability:**
- No crashes or freezes
- Memory usage stable (<200MB)
- API errors handled gracefully
- Works on 95%+ of websites
- No security vulnerabilities

✅ **Documentation:**
- README explains installation
- USER_GUIDE covers all features
- TROUBLESHOOTING addresses common issues
- Code is commented and maintainable

---

## 🏆 TESTING COMPLETION CHECKLIST

### Domain Warnings:
- [ ] Fake domain warning (naturalnews.com)
- [ ] Trusted domain badge (cdc.gov)
- [ ] No warning on neutral sites (google.com)
- [ ] Close button works
- [ ] Auto-dismiss trusted warnings (5s)
- [ ] Mobile responsive styling

### Keyboard Shortcuts:
- [ ] Ctrl+Shift+V triggers quick scan
- [ ] Ctrl+Shift+S toggles sidebar
- [ ] Ctrl+Shift+H toggles highlights
- [ ] Notifications appear
- [ ] Badge updates correctly

### Statistics:
- [ ] Scans are recorded
- [ ] Fake items counted correctly
- [ ] History stored (last 100)
- [ ] Summary calculations accurate
- [ ] Export works (JSON)

### Integration:
- [ ] All features work together
- [ ] No conflicts or bugs
- [ ] Performance is acceptable
- [ ] Memory usage is stable
- [ ] Backend communication reliable

---

Generated: 2025-01-XX  
Version: 1.0  
Status: ✅ READY FOR TESTING
