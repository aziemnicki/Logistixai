#!/usr/bin/env python3
"""
Quick test script to verify font registration works correctly.
Run this from the services directory to test fonts without starting the full backend.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("\n" + "="*60)
print("🔤 FONT REGISTRATION TEST")
print("="*60)

# This will trigger font registration
from services.pdf_service import _registered_fonts, _missing_fonts, get_font_name

print("\n📊 Test Results:")
print(f"   Registered fonts: {len(_registered_fonts)}/5")
print(f"   Missing fonts: {len(_missing_fonts)}/5")

print("\n✅ Registered Fonts:")
for font in _registered_fonts:
    print(f"   ✓ {font}")

if _missing_fonts:
    print("\n❌ Missing Fonts:")
    for font in _missing_fonts:
        print(f"   ✗ {font}")

print("\n🎨 Font Mappings (with fallback):")
test_mappings = [
    ("Inter-Bold", "Title/Heading font"),
    ("Inter-SemiBold", "Section heading font"),
    ("Inter-Medium", "Subheading font"),
    ("IBMPlexSans", "Body text font"),
    ("IBMPlexSans-Bold", "Bold text/Risk labels"),
]

for preferred, description in test_mappings:
    actual = get_font_name(preferred)
    status = "✓" if actual == preferred else "→"
    print(f"   {status} {preferred:20} → {actual:20} ({description})")

print("\n" + "="*60)

# Final verdict
if len(_registered_fonts) == 5:
    print("🎉 SUCCESS! All custom fonts loaded correctly!")
    print("   Your PDFs will use Inter for headings and IBM Plex Sans for body text.")
elif len(_registered_fonts) > 0:
    print("⚠️  PARTIAL: Some fonts loaded, others using Helvetica fallback.")
    print("   PDFs will still generate but some fonts will be substituted.")
else:
    print("❌ WARNING: No custom fonts loaded, using Helvetica fallback.")
    print("   PDFs will generate but won't use custom fonts.")

print("="*60 + "\n")
