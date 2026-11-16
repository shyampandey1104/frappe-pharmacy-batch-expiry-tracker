# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "pharma"
app_title = "Frappe Pharmacy Batch Expiry Tracker"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Pharmacy Batch Expiry Tracker for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/pharma/css/pharma.bundle.css"
app_include_js = "/assets/pharma/js/pharma.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "pharma.engine.on_document_submit",
        "on_cancel": "pharma.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "pharma.engine.daily_scheduled_sync"
    ]
}
