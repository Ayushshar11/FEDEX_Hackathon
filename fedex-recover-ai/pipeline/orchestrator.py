import logging

# Configure logging for audit trails
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Orchestrator")

def ai_decision_engine(recovery_score: float, amount: float, days_overdue: int) -> dict:
    """
    Translates AI inference results into operational business constraints.
    """
    # High-Performance Tier
    if recovery_score >= 80:
        return {
            "agency": "Tier 1: Strategic Recovery",
            "priority": "P1 - Critical",
            "sla_hours": 24,
            "action": "Direct agent intervention / Legal notice prep",
            "risk_level": "Low Risk / High Yield"
        }

    # Standard Operations Tier
    elif recovery_score >= 50:
        return {
            "agency": "Tier 2: Standard Collections",
            "priority": "P2 - Elevated",
            "sla_hours": 48,
            "action": "Multi-channel outreach (Phone/Email)",
            "risk_level": "Moderate Risk"
        }

    # Low-Touch / Automated Tier
    else:
        return {
            "agency": "Tier 3: Automated Workflow",
            "priority": "P3 - Standard",
            "sla_hours": 72,
            "action": "Automated digital dunning / Periodic review",
            "risk_level": "High Risk / Contingent"
        }

def check_sla(hours_passed: int, sla_limit: int) -> dict:
    """
    Evaluates operational compliance against defined agency SLAs.
    """
    is_breached = hours_passed > sla_limit
    return {
        "status": "NON-COMPLIANT" if is_breached else "COMPLIANT",
        "breach_flag": is_breached,
        "indicator": "🔴" if is_breached else "🟢"
    }

def update_dca_performance_index(current_index: int, sla_breach: bool, success: bool) -> int:
    """
    Dynamic scoring algorithm for agency performance evaluation.
    """
    adjustment = 0
    if sla_breach:
        adjustment -= 15
    if success:
        adjustment += 10

    return max(0, min(100, current_index + adjustment))

def orchestrate_case(ai_prob: float, amount: float, days_overdue: int, elapsed: int, dca_rank: int) -> dict:
    """
    Primary Orchestration Hub: Aggregates AI intelligence with business logic.
    """
    score = ai_prob * 100
    
    # 1. Logic Trigger
    decision = ai_decision_engine(score, amount, days_overdue)
    
    # 2. Compliance Check
    compliance = check_sla(elapsed, decision["sla_hours"])
    
    # 3. Performance Update
    new_rank = update_dca_performance_index(dca_rank, compliance["breach_flag"], False)

    logger.info(f"Case Processed - Score: {score:.2f} | Status: {compliance['status']}")

    return {
        "propensity_score": round(score, 2),
        "allocation": decision,
        "compliance_audit": compliance,
        "adjusted_performance_index": new_rank
    }