# ⚖️ LexWatch, AI Powered Regulatory Compliance Agent

> Built for UiPath AgentHack 2026 | Track 1: UiPath Maestro Case

LexWatch is an enterprise-grade agentic compliance system that continuously monitors global regulatory bodies, classifies updates using AI, detects policy gaps, and orchestrates case-based workflows with human approval gates, all powered by UiPath Maestro Case.

---

## 🚨 The Problem

Compliance officers at financial institutions manually monitor dozens of regulatory bodies (FCA, SEC, BIS, FATF, and more) for new publications. When a new regulation drops, they manually:

- Read and interpret the update
- Assess its impact on the business
- Cross-reference it against internal policies
- Route tasks to Legal, Risk, Compliance, and Operations teams
- Track progress and maintain an audit trail

This process takes **days to weeks**, is **error-prone**, and creates **compliance gaps** that expose organizations to regulatory fines and reputational damage.

---

## ✅ The Solution

LexWatch automates the entire regulatory change management lifecycle using 4 AI agents orchestrated by UiPath Maestro Case:
Agent 1: Scraper Agent → Monitors live regulatory RSS feeds

Agent 2: Classifier Agent → LLM classifies impact level and affected departments

Agent 3: Policy Matcher → Detects gaps between new regulations and internal policies

Agent 4: Case Manager → Creates and routes Maestro cases to the right teams
---

## 🏗️ Architecture
[Regulatory Sources] → FCA, BIS, SEC, FATF (live RSS feeds)

↓

[Scraper Agent] → Collects and normalizes regulatory updates

↓

[Classifier Agent] → Groq LLM assesses impact: CRITICAL/HIGH/MEDIUM/LOW

↓

[Policy Matcher Agent] → Cross-references against 6 internal company policies

↓

[UiPath Maestro Case] → Creates cases, routes to teams, tracks human approvals

↓

[Human Approval Gates] → Legal → Risk → Compliance → CCO → Operations

↓

[Audit Trail] → Full case history saved and archived
---

## 🎯 UiPath Components Used

- **UiPath Maestro Case**: Core orchestration and case management layer
- **UiPath Agent Builder**: Wraps Python agents for platform integration
- **UiPath API Workflows**: Connects to external regulatory data sources
- **UiPath Automation Cloud**: Hosts and runs the entire solution

> 🤖 **Bonus:** This solution was built using **Claude Code** (UiPath for Coding Agents), earning additional judging points under the Platform Usage criterion.

## Agent Type

LexWatch uses **Coded Agents** built with the UiPath Python SDK and 
the Groq LLM API. All four agents (Scraper, Classifier, Policy Matcher, 
and Case Manager) are coded agents written in Python. The BPMN 
orchestration flow is built using UiPath Maestro BPMN on UiPath 
Automation Cloud. This solution combines coded agents with low-code 
BPMN orchestration for a hybrid approach.

---

## 🗂️ Project Structure
lexwatch/

├── agents/

│   ├── scraper_agent.py      # Regulatory RSS feed monitor

│   ├── classifier_agent.py   # Groq LLM impact classifier

│   ├── policy_matcher.py     # Internal policy gap detector

│   └── case_manager.py       # Maestro case creator and router

├── data/

│   ├── cases.json            # Generated case records

│   └── sample_policies/      # Internal policy documents

├── tests/                    # Test suite

├── main.py                   # Main orchestrator

├── config.py                 # Configuration and settings

├── requirements.txt          # Python dependencies

└── .env.example              # Environment variable template
---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.12+
- GitHub Codespaces or local environment
- UiPath Automation Cloud account (via UiPath Labs)
- Groq API key (free at https://console.groq.com)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/sirmos/lexwatch.git
cd lexwatch
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
GROQ_API_KEY=your_groq_api_key_here

UIPATH_CLIENT_ID=your_uipath_client_id

UIPATH_CLIENT_SECRET=your_uipath_client_secret

UIPATH_TENANT_NAME=your_tenant_name

UIPATH_ORG_ID=your_org_id
**4. Run LexWatch**
```bash
python main.py
```

---

## 🔄 How It Works

1. **Scraper Agent** monitors 4 live regulatory sources every cycle
2. **Classifier Agent** sends each update to Groq LLM for impact assessment
3. **Policy Matcher** cross-references updates against 6 internal policies
4. **Case Manager** creates a Maestro case for every update with policy conflicts
5. Each case flows through **7 stages** with human approval gates:
   - Stage 1: Intake & Classification *(AI Agent)*
   - Stage 2: Legal Review *(Legal Team)*
   - Stage 3: Risk Assessment *(Risk Team)*
   - Stage 4: Policy Update *(Compliance Team)*
   - Stage 5: Senior Approval *(Chief Compliance Officer)*
   - Stage 6: Implementation *(Operations Team)*
   - Stage 7: Case Closed *(AI Agent)*

---

## 🏆 Business Impact

| Metric | Before LexWatch | After LexWatch |
|--------|----------------|----------------|
| Time to detect new regulation | Days | Minutes |
| Policy gap identification | Manual, error-prone | Automated, AI-powered |
| Case routing time | Hours | Seconds |
| Audit trail | Spreadsheets | Automated, real-time |
| Compliance officer workload | High | Reduced by ~80% |

---

## 🌍 Regulatory Sources Monitored

- **FCA** — UK Financial Conduct Authority
- **BIS** — Bank for International Settlements  
- **SEC** — US Securities and Exchange Commission
- **FATF** — Financial Action Task Force

---

## 📋 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built with ❤️ for UiPath AgentHack 2026  
Track: UiPath Maestro Case  
Location: Akwa Ibom, Nigeria 🇳🇬

## Agent Type

LexWatch uses **Coded Agents** built with the UiPath Python SDK and the Groq LLM API. All four agents (Scraper, Classifier, Policy Matcher, and Case Manager) are coded agents written in Python. The BPMN orchestration flow is built using UiPath Maestro BPMN on UiPath Automation Cloud. This solution combines coded agents with low-code BPMN orchestration for a hybrid approach.
