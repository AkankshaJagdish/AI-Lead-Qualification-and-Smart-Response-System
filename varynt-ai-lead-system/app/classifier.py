def classify(score: int) -> str:
    if score >= 70:
        return "HOT"
    if score >= 40:
        return "WARM"
    return "COLD"
