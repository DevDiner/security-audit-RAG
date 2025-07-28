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

    if "delegatecall" in code or "DELEGATECALL" in code:
        score += 10
    else:
        issues.append({"issue": "No Delegatecall Proxy Pattern", "risk": "Medium"})

    if any(x in code for x in ["ERC20", "IERC20"]):
        score += 10
    elif any(x in code for x in ["ERC721", "IERC721"]):
        score += 10
    elif any(x in code for x in ["ERC1155", "IERC1155"]):
        score += 10
    else:
        issues.append({"issue": "No recognized ERC standard (ERC20/721/1155)", "risk": "Medium"})

    return score, issues
