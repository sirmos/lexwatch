import sys
sys.path.insert(0, '/home/user/workspace')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.scraper_agent import ScraperAgent
from agents.classifier_agent import ClassifierAgent
from agents.policy_matcher import PolicyMatcherAgent
from agents.case_manager import CaseManagerAgent
import uvicorn

app = FastAPI(
    title="LexWatch API",
    description="AI-Powered Regulatory Compliance Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "name": "LexWatch",
        "version": "1.0.0",
        "status": "running",
        "description": "AI-Powered Regulatory Compliance Agent"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/run")
def run_lexwatch():
    try:
        # Stage 1: Scrape
        scraper = ScraperAgent()
        updates = scraper.run()

        # Stage 2: Classify
        classifier = ClassifierAgent()
        classifications = classifier.run(updates)

        # Stage 3: Policy Match
        matcher = PolicyMatcherAgent()
        all_matches = matcher.run(updates, classifications)

        # Stage 4: Create Cases
        manager = CaseManagerAgent()
        cases = manager.run(updates, classifications, all_matches)

        return {
            "status": "success",
            "updates_scraped": len(updates),
            "conflicts_detected": sum(len(m) for m in all_matches.values()),
            "cases_created": len(cases),
            "cases": [c.to_dict() for c in cases]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/scrape")
def scrape_only():
    try:
        scraper = ScraperAgent()
        updates = scraper.run()
        return {
            "status": "success",
            "updates_found": len(updates),
            "updates": [u.dict() for u in updates]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
