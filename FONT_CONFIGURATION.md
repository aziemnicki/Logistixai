# 🔤 Font Configuration Guide

## ✅ Font Setup Complete

Your PDF service is now configured to use:
- **Inter fonts** for headings and subheadings
- **IBM Plex Sans** for body text

---

## 📁 Font Files Detected

Located in `backend/services/`:
```
✓ IBMPlexSans-Light.ttf       → Body text
✓ IBMPlexSans-Bold.ttf         → Bold body text, risk labels
✓ Inter_18pt-Bold.ttf          → Main headings
✓ Inter_18pt-SemiBold.ttf      → Section headings
✓ Inter_18pt-Medium.ttf        → Subheadings
```

---

## 🎨 Font Mapping

### Headings (Inter Family)
| Style | Font | Usage |
|-------|------|-------|
| **CustomTitle** | Inter-Bold | Main report title |
| **SectionHeader** | Inter-Bold | Major sections (Summary, Legal Changes, etc.) |
| **Section** | Inter-SemiBold | Section headings |
| **SubSection** | Inter-Medium | Subsection headings |

### Body Text (IBM Plex Sans)
| Style | Font | Usage |
|-------|------|-------|
| **Normal** | IBMPlexSans | Regular paragraph text |
| **BodyText** | IBMPlexSans | Body content |
| **Risk Labels** | IBMPlexSans-Bold | Critical/High/Medium/Low labels |

---

## 🔧 What Was Fixed

### Problem 1: Hardcoded Relative Paths ❌
**Before:**
```python
pdfmetrics.registerFont(TTFont('IBMPlexSans', 'Logistic_simple\\backend\\services\\IBMPlexSans-Light.ttf'))
```
- Would only work from specific working directory
- Failed when running from different locations

**After:** ✅
```python
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, 'IBMPlexSans-Light.ttf')
pdfmetrics.registerFont(TTFont('IBMPlexSans', font_path))
```
- Uses absolute paths
- Works from any working directory

### Problem 2: No Fallback Handling ❌
**Before:**
```python
fontName='Inter-Bold'  # Fails if font not loaded
```

**After:** ✅
```python
fontName=get_font_name('Inter-Bold', 'Helvetica-Bold')  # Falls back to Helvetica-Bold
```
- Automatically falls back to Helvetica if custom fonts fail
- PDF always generates successfully

### Problem 3: Silent Failures ❌
**Before:**
- Fonts failed to load with generic error
- No visibility into which fonts worked

**After:** ✅
- Clear console output showing each font registration
- Lists missing fonts
- Shows registration summary

---

## 📊 Expected Console Output

When the backend starts, you'll see:

### ✅ Success Case (All Fonts Loaded)
```
🔤 Font Registration:
   ✓ IBMPlexSans: IBMPlexSans-Light.ttf
   ✓ IBMPlexSans-Bold: IBMPlexSans-Bold.ttf
   ✓ Inter-Bold: Inter_18pt-Bold.ttf
   ✓ Inter-SemiBold: Inter_18pt-SemiBold.ttf
   ✓ Inter-Medium: Inter_18pt-Medium.ttf
   ✅ Successfully registered 5/5 fonts
```

### ⚠️ Partial Failure (Some Fonts Missing)
```
🔤 Font Registration:
   ✓ IBMPlexSans: IBMPlexSans-Light.ttf
   ✓ IBMPlexSans-Bold: IBMPlexSans-Bold.ttf
   ✗ Inter-Bold: File not found at C:\...\Inter_18pt-Bold.ttf
   ✗ Inter-SemiBold: File not found at C:\...\Inter_18pt-SemiBold.ttf
   ✗ Inter-Medium: File not found at C:\...\Inter_18pt-Medium.ttf
   ✅ Successfully registered 2/5 fonts
   ⚠️  3 fonts unavailable, will use fallback (Helvetica)
   📝 Missing: Inter-Bold, Inter-SemiBold, Inter-Medium
```

In this case:
- Body text uses IBM Plex Sans ✅
- Headings use Helvetica-Bold (fallback) 🔄

---

## 🧪 Testing Font Configuration

### 1. Start Backend
```bash
cd backend
python main.py
```

**Look for the "🔤 Font Registration" output in the console.**

### 2. Generate PDF
```bash
curl -X POST http://localhost:8000/api/reports/generate
```

### 3. Check PDF Fonts
Open the generated PDF in Adobe Reader:
1. **File → Properties → Fonts tab**
2. You should see:
   - `Inter-Bold (Embedded Subset)`
   - `Inter-SemiBold (Embedded Subset)`
   - `Inter-Medium (Embedded Subset)`
   - `IBMPlexSans (Embedded Subset)`
   - `IBMPlexSans-Bold (Embedded Subset)`

If you see `Helvetica` instead, the custom fonts failed to load.

---

## 🔍 Troubleshooting

### Issue: Fonts Show as "Helvetica" in PDF

**Possible causes:**

1. **Font files missing**
   ```bash
   # Check if files exist
   ls backend/services/*.ttf
   ```
   Should show all 5 `.ttf` files.

2. **Corrupted font files**
   Re-download fonts:
   - [Inter fonts](https://fonts.google.com/specimen/Inter)
   - [IBM Plex Sans](https://fonts.google.com/specimen/IBM+Plex+Sans)

3. **Permission issues**
   ```bash
   # Ensure files are readable
   chmod 644 backend/services/*.ttf
   ```

4. **ReportLab version issue**
   ```bash
   pip install --upgrade reportlab
   ```

### Issue: "TTFont ... not found in registry"

**Solution:** The `get_font_name()` function should prevent this, but if you see it:

1. Check console output for font registration errors
2. Verify font file names match exactly:
   - `IBMPlexSans-Light.ttf` (not `IBMPlexSans-Regular.ttf`)
   - `Inter_18pt-Bold.ttf` (not `Inter-Bold.ttf`)

### Issue: Fonts work locally but fail in production

**Solution:** Ensure font files are included in deployment:
```bash
# If using Git, ensure .ttf files are not ignored
git add -f backend/services/*.ttf
```

---

## 📐 Font Specifications

### Inter Font
- **Family:** Inter
- **Weights Used:**
  - Bold (700) → Main headings
  - SemiBold (600) → Section headings
  - Medium (500) → Subheadings
- **Character Set:** Latin Extended
- **OpenType Features:** Used at 18pt scale

### IBM Plex Sans
- **Family:** IBM Plex Sans
- **Weights Used:**
  - Light (300) → Body text
  - Bold (700) → Risk labels, emphasis
- **Character Set:** Latin Extended
- **Designed For:** Screen and print readability

---

## 🎨 Visual Hierarchy

```
┌─────────────────────────────────────────┐
│ Logistics Compliance Report            │ ← Inter-Bold 20pt
│                                         │
├─────────────────────────────────────────┤
│ Executive Summary                       │ ← Inter-Bold 14pt
├─────────────────────────────────────────┤
│                                         │
│ Key Takeaways:                         │ ← Inter-Medium 11pt
│ • Regular body text content about...   │ ← IBMPlexSans 10pt
│ • More information in body text...     │
│                                         │
│ Risk Level: Critical                   │ ← IBMPlexSans-Bold 10pt (Red)
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔄 Fallback Strategy

The system uses a 3-tier fallback:

1. **First Choice:** Custom fonts (Inter, IBM Plex Sans)
2. **Second Choice:** Helvetica family (if custom fonts fail)
3. **Final Fallback:** System default serif font

```python
# Automatic fallback logic
get_font_name('Inter-Bold', 'Helvetica-Bold')
```

This ensures PDFs **always generate successfully**, even if custom fonts are unavailable.

---

## ✅ Success Criteria

Your fonts are working correctly if:

✅ Console shows "Successfully registered 5/5 fonts"
✅ PDF properties show custom fonts (not Helvetica)
✅ Headings look distinct from body text
✅ Text is crisp and readable at all zoom levels
✅ PDF file size is reasonable (< 500KB for typical reports)

---

## 📝 Adding New Fonts

To add additional font weights or families:

1. **Add font file** to `backend/services/`:
   ```bash
   cp Inter_18pt-Light.ttf backend/services/
   ```

2. **Register in pdf_service.py**:
   ```python
   fonts_to_register = [
       # ... existing fonts ...
       ('Inter-Light', 'Inter_18pt-Light.ttf'),  # Add this line
   ]
   ```

3. **Use in styles**:
   ```python
   add_style('LightText', fontName=get_font_name('Inter-Light', 'Helvetica'))
   ```

4. **Restart backend** to load new fonts

---

## 🎉 Summary

**Your PDF service now:**
- ✅ Uses Inter for all headings (Bold, SemiBold, Medium)
- ✅ Uses IBM Plex Sans for body text (Light, Bold)
- ✅ Automatically falls back to Helvetica if fonts unavailable
- ✅ Shows clear console output for debugging
- ✅ Works from any working directory (absolute paths)
- ✅ Handles missing fonts gracefully

**Test it:** Generate a report and check the console output! 🚀
