import os

# =====================================
# Application
# =====================================

APP_NAME = "GlowGuide"

PAGE_TITLE = "GlowGuide | Precision Matrix"

PAGE_ICON = "🌿"

LAYOUT = "centered"

# =====================================
# Database
# =====================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "skincare.db")

# =====================================
# Session
# =====================================

MAX_HISTORY = 5

# =====================================
# Theme
# =====================================

PRIMARY_GREEN = "#2E5A36"

BACKGROUND = "#F8FAFC"

TEXT = "#1E293B"