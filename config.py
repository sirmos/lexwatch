import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Anthropic
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # UiPath
    UIPATH_CLIENT_ID = os.getenv("UIPATH_CLIENT_ID", "")
    UIPATH_CLIENT_SECRET = os.getenv("UIPATH_CLIENT_SECRET", "")
    UIPATH_TENANT_NAME = os.getenv("UIPATH_TENANT_NAME", "")
    UIPATH_ORG_ID = os.getenv("UIPATH_ORG_ID", "")

    # Regulatory sources to monitor
    REGULATORY_SOURCES = [
        {
            "name": "SEC (US Securities and Exchange Commission)",
            "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=&dateb=&owner=include&count=10&search_text=",
            "rss": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=&dateb=&owner=include&count=10&output=atom",
            "jurisdiction": "US",
            "category": "Securities"
        },
        {
            "name": "FCA (UK Financial Conduct Authority)",
            "url": "https://www.fca.org.uk/news",
            "rss": "https://www.fca.org.uk/rss.xml",
            "jurisdiction": "UK",
            "category": "Financial"
        },
        {
            "name": "BIS (Bank for International Settlements)",
            "url": "https://www.bis.org/list/speeches/index.htm",
            "rss": "https://www.bis.org/doclist/bis_fsi_publs.rss",
            "jurisdiction": "Global",
            "category": "Banking"
        },
        {
            "name": "FATF (Financial Action Task Force)",
            "url": "https://www.fatf-gafi.org/en/publications.html",
            "rss": "https://www.fatf-gafi.org/en/publications.rss",
            "jurisdiction": "Global",
            "category": "AML/CFT"
        }
    ]

    # Impact levels
    IMPACT_LEVELS = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    # Departments to route to
    DEPARTMENTS = ["Legal", "Risk", "Compliance", "Operations", "Finance"]

    # App settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

config = Config()
