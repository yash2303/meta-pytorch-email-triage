"""Hardcoded email datasets for each task with ground-truth labels."""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class EmailSample:
    subject: str
    body: str
    sender: str
    metadata: Dict[str, Any]
    # Ground truth
    category: str
    priority: str
    department: str


# ---------------------------------------------------------------------------
# TASK 1: basic_triage  (easy — clear-cut emails)
# ---------------------------------------------------------------------------
BASIC_TRIAGE_EMAILS: List[EmailSample] = [
    EmailSample(
        subject="Invoice #4821 overdue – payment needed",
        body=(
            "Hi,\n\nInvoice #4821 for $2,340 was due on March 15. "
            "Please process the payment at your earliest convenience to "
            "avoid a late fee.\n\nBest,\nAccounts Receivable"
        ),
        sender="billing@vendorcorp.com",
        metadata={"has_attachment": True, "attachment_name": "invoice_4821.pdf"},
        category="billing",
        priority="high",
        department="finance",
    ),
    EmailSample(
        subject="VPN not connecting from home",
        body=(
            "Hello IT,\n\nI've been unable to connect to the company VPN "
            "since this morning. I've tried restarting my laptop and router. "
            "Error message: 'Connection timed out'. I need VPN access to "
            "do my work.\n\nThanks,\nDave"
        ),
        sender="dave.wilson@company.com",
        metadata={"has_attachment": False},
        category="technical",
        priority="high",
        department="engineering",
    ),
    EmailSample(
        subject="Request for annual leave – April 10-14",
        body=(
            "Hi HR,\n\nI'd like to request annual leave from April 10 to "
            "April 14 (5 days). I have sufficient leave balance. "
            "Please let me know if approved.\n\nRegards,\nSarah Chen"
        ),
        sender="sarah.chen@company.com",
        metadata={"has_attachment": False},
        category="hr",
        priority="low",
        department="hr",
    ),
    EmailSample(
        subject="New product demo request for Q2",
        body=(
            "Hi Sales Team,\n\nWe're interested in scheduling a demo of "
            "your Enterprise Analytics platform. We have a team of 50 users "
            "and are evaluating solutions for Q2 rollout. Can we schedule "
            "a call next week?\n\nBest,\nMartin Blake\nCTO, DataFlow Inc."
        ),
        sender="martin@dataflow.io",
        metadata={"has_attachment": False},
        category="sales",
        priority="medium",
        department="sales",
    ),
    EmailSample(
        subject="Office Wi-Fi password for guest network",
        body=(
            "Hello,\n\nCould someone share the current guest Wi-Fi password? "
            "We have a client visiting tomorrow and want them to have "
            "internet access.\n\nThanks,\nReception Desk"
        ),
        sender="reception@company.com",
        metadata={"has_attachment": False},
        category="general",
        priority="low",
        department="support",
    ),
]

# ---------------------------------------------------------------------------
# TASK 2: ambiguous_triage  (medium — requires inference)
# ---------------------------------------------------------------------------
AMBIGUOUS_TRIAGE_EMAILS: List[EmailSample] = [
    EmailSample(
        subject="Unhappy with recent charges",
        body=(
            "To whom it may concern,\n\nI was charged twice for my "
            "subscription renewal this month. I noticed $49.99 billed "
            "on March 1 and again on March 3. This is frustrating because "
            "I've been a loyal customer for 3 years. Please refund the "
            "duplicate charge immediately or I will dispute with my bank."
            "\n\nAngry customer,\nJamie Torres"
        ),
        sender="jamie.torres@gmail.com",
        metadata={"has_attachment": True, "attachment_name": "bank_statement.png"},
        category="billing",
        priority="critical",
        department="finance",
    ),
    EmailSample(
        subject="Can't access my account after update",
        body=(
            "Hi,\n\nAfter your latest app update (v4.2.1), I'm locked out "
            "of my account. The login page just shows a spinner and then "
            "crashes. I tried clearing cache and reinstalling. This is urgent "
            "because I need to approve a purchase order by end of day. "
            "My employee ID is 84723.\n\nPlease help,\nLisa Park"
        ),
        sender="lisa.park@company.com",
        metadata={"has_attachment": False},
        category="technical",
        priority="critical",
        department="engineering",
    ),
    EmailSample(
        subject="Team lunch budget question",
        body=(
            "Hey,\n\nOur team wants to organize a lunch for a departing "
            "colleague. Is there a company budget for farewell events? "
            "Also, can we expense this through the regular team-building "
            "allowance, or do we need a separate approval? About 15 people.\n\n"
            "Cheers,\nAlex"
        ),
        sender="alex.kumar@company.com",
        metadata={"has_attachment": False},
        category="hr",
        priority="low",
        department="finance",
    ),
    EmailSample(
        subject="Re: Partnership opportunity",
        body=(
            "Following up on our conversation at the Tech Summit — "
            "our company (500+ employees) is looking for a vendor to handle "
            "our cloud infrastructure migration. We've budgeted $200K for "
            "this project and need to start by Q3. Could you send over a "
            "proposal and pricing tiers?\n\nRegards,\nPriya Sharma\n"
            "VP Operations, NovaTech"
        ),
        sender="priya.sharma@novatech.com",
        metadata={"has_attachment": False},
        category="sales",
        priority="high",
        department="sales",
    ),
    EmailSample(
        subject="Broken desk chair – ergonomics concern",
        body=(
            "Hi Facilities,\n\nMy desk chair's lumbar support is broken "
            "and the armrest fell off yesterday. I've been having back pain "
            "as a result. Could you please arrange a replacement? I sit at "
            "desk 4B-12 on the 4th floor. My manager said this should be "
            "covered under our workplace safety policy.\n\nThanks,\nMark"
        ),
        sender="mark.johnson@company.com",
        metadata={"has_attachment": True, "attachment_name": "broken_chair.jpg"},
        category="general",
        priority="medium",
        department="support",
    ),
]

# ---------------------------------------------------------------------------
# TASK 3: complex_triage  (hard — multi-topic, edge cases)
# ---------------------------------------------------------------------------
COMPLEX_TRIAGE_EMAILS: List[EmailSample] = [
    EmailSample(
        subject="Quarterly review + budget concerns + system issues",
        body=(
            "Hi team,\n\n"
            "Three things:\n\n"
            "1. Our Q1 quarterly review is scheduled for April 5. Please "
            "prepare your team's metrics by April 3.\n\n"
            "2. We're 15% over budget on the infrastructure project. The "
            "additional AWS costs ($18K) were not in the original estimate. "
            "Finance needs to approve the overage ASAP or we'll have to "
            "pause the project.\n\n"
            "3. Also, the staging environment has been down since yesterday. "
            "Deployments are blocked. Can someone from engineering look into "
            "this urgently?\n\n"
            "Thanks,\nDirector of Engineering"
        ),
        sender="director.eng@company.com",
        metadata={"has_attachment": True, "attachment_name": "q1_budget_report.xlsx"},
        category="technical",
        priority="critical",
        department="engineering",
    ),
    EmailSample(
        subject="FW: [External] Compliance audit findings",
        body=(
            "Forwarding the findings from our PCI compliance audit. They "
            "flagged three critical items:\n\n"
            "- Credit card data stored in plaintext in the legacy billing DB\n"
            "- Missing access logs for the payment processing server\n"
            "- Two employees still have admin access after leaving the company\n\n"
            "The auditor says we have 30 days to remediate before our "
            "certification is revoked. This affects our ability to process "
            "payments.\n\nAction required immediately.\n\n"
            "— Legal & Compliance Team"
        ),
        sender="compliance@company.com",
        metadata={"has_attachment": True, "attachment_name": "audit_report_pci.pdf"},
        category="technical",
        priority="critical",
        department="engineering",
    ),
    EmailSample(
        subject="hey quick question",
        body=(
            "yo,\n\n"
            "my paycheck this month looked weird. i think taxes were taken "
            "out wrong? also my manager said i was supposed to get the "
            "senior title update but my email signature still says 'associate'. "
            "who do i talk to about both of these things? btw the vending "
            "machine on floor 3 ate my dollar again lol\n\n"
            "- Jake"
        ),
        sender="jake.martinez@company.com",
        metadata={"has_attachment": False},
        category="hr",
        priority="medium",
        department="hr",
    ),
    EmailSample(
        subject="URGENT: Client threatening to leave",
        body=(
            "URGENT\n\n"
            "AccuHealth (our 2nd largest client, $450K ARR) just informed "
            "us they're evaluating competitors. Their pain points:\n"
            "1. Three outages in the past month (SRE issue)\n"
            "2. Feature requests from 6 months ago still undelivered\n"
            "3. Their invoice from February had incorrect charges\n\n"
            "They want a call with our VP by Friday or they're starting "
            "the migration process to a competitor. We CANNOT lose this "
            "account.\n\n"
            "— Account Manager, Enterprise Team"
        ),
        sender="enterprise.am@company.com",
        metadata={"has_attachment": True, "attachment_name": "accuhealth_account_summary.pdf"},
        category="sales",
        priority="critical",
        department="sales",
    ),
    EmailSample(
        subject="Re: Re: Re: building access card not working (3rd request)",
        body=(
            "This is my THIRD time emailing about this. My building access "
            "card stopped working two weeks ago. I've been having to tailgate "
            "other employees to get into the office, which I know is a "
            "security violation. My manager escalated this last week and "
            "there's been no response. I work in the secure data center "
            "area and technically should not be entering without my own "
            "badge scan for audit purposes.\n\n"
            "This is now a security issue, not just a convenience problem.\n\n"
            "— Frustrated Employee #67892"
        ),
        sender="emp67892@company.com",
        metadata={"has_attachment": False},
        category="general",
        priority="critical",
        department="support",
    ),
]

# ---------------------------------------------------------------------------
# Task registry
# ---------------------------------------------------------------------------
TASKS = {
    "basic_triage": {
        "difficulty": "easy",
        "description": "Clear-cut emails with obvious category, priority, and department.",
        "emails": BASIC_TRIAGE_EMAILS,
    },
    "ambiguous_triage": {
        "difficulty": "medium",
        "description": "Emails requiring inference — intent may not match surface wording.",
        "emails": AMBIGUOUS_TRIAGE_EMAILS,
    },
    "complex_triage": {
        "difficulty": "hard",
        "description": "Multi-topic emails, edge cases, urgency buried in context.",
        "emails": COMPLEX_TRIAGE_EMAILS,
    },
}

# Valid value sets for scoring
VALID_CATEGORIES = {"billing", "technical", "hr", "sales", "general"}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}
VALID_DEPARTMENTS = {"engineering", "finance", "hr", "sales", "support"}

# Priority distance for partial credit
PRIORITY_ORDER = ["low", "medium", "high", "critical"]
