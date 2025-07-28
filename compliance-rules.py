def check_compliance(code: str):
    score = 0
    issues = []

    if "Ownable" in code or "AccessControl" in code:
        score += 20
    else:
        issues.append({"issue": "Missing Ownable or AccessControl", "risk": "High"})

    if "Pausable" in code:
        score += 15
    else:
        issues.append({"issue": "No Pausable Mechanism", "risk": "Medium"})

    if "nonReentrant" in code:
        score += 15
    else:
        issues.append({"issue": "Missing Reentrancy Guard", "risk": "High"})

    if "UUPSUpgradeable" in code or "TransparentUpgradeableProxy" in code:
        score += 10
    else:
        issues.append({"issue": "Not Upgradeable", "risk": "Low"})

    if "ERC20" in code:
        score += 10
    elif "ERC721" in code or "ERC1155" in code:
        score += 10
    else:
        issues.append({"issue": "No recognized ERC standard", "risk": "Medium"})

    return score, issues
