from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
import math

from .config import THRESHOLDS

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def score_to_level(score: float) -> str:
    if score < THRESHOLDS.low:
        return "LOW"
    if score < THRESHOLDS.medium:
        return "MEDIUM"
    if score < THRESHOLDS.high:
        return "HIGH"
    return "EXTREME"

def level_to_recommendation(level: str) -> str:
    return {
        "LOW": "الوضع طبيعي. راقب فقط.",
        "MEDIUM": "انتبه: تجنب مصادر الشرر وراقب المنطقة.",
        "HIGH": "خطر مرتفع: فعّل المراقبة ومنع إشعال النار في المناطق الحساسة.",
        "EXTREME": "خطر شديد: إجراءات فورية، تنبيه الجهات، وتقييد الوصول للمناطق عالية الخطورة.",
    }.get(level, "اتبع إجراءات السلامة.")

@dataclass
class RiskResult:
    risk_score: float
    risk_level: str
    explanation: str
    recommendation: str
