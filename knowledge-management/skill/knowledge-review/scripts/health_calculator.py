#!/usr/bin/env python3
"""
health_calculator.py — 知识库健康度计算

用法:
    python3 health_calculator.py --p0 2 --p1 3 --p2 5
    
输出:
    健康度评分和评级
"""
import sys
import json
import argparse


# ============================================================
# 健康度配置（内联，不依赖外部 constants.py）
# ============================================================

HEALTH_PENALTY = {
    "P0": {"weight": 20, "max": 40},  # 每个P0问题扣20分，上限40分
    "P1": {"weight": 10, "max": 30},  # 每个P1问题扣10分，上限30分
    "P2": {"weight": 5,  "max": 20},  # 每个P2问题扣5分，上限20分
}

HEALTH_GRADES = [
    (80, 100, "healthy",           "🟢 健康"),
    (60, 79,  "needs_attention",   "🟡 需关注"),
    (0,  59,  "needs_optimization", "🔴 需优化"),
]


def calculate_health(p0_count: int, p1_count: int, p2_count: int) -> dict:
    """计算健康度评分和评级"""
    score = 100
    
    # 计算扣分
    p0_penalty = min(p0_count * HEALTH_PENALTY["P0"]["weight"], HEALTH_PENALTY["P0"]["max"])
    p1_penalty = min(p1_count * HEALTH_PENALTY["P1"]["weight"], HEALTH_PENALTY["P1"]["max"])
    p2_penalty = min(p2_count * HEALTH_PENALTY["P2"]["weight"], HEALTH_PENALTY["P2"]["max"])
    
    score -= (p0_penalty + p1_penalty + p2_penalty)
    score = max(0, score)
    
    # 确定评级
    grade_key = "needs_optimization"
    grade_label = "🔴 需优化"
    for min_score, max_score, key, label in HEALTH_GRADES:
        if min_score <= score <= max_score:
            grade_key = key
            grade_label = label
            break
    
    return {
        "score": score,
        "grade_key": grade_key,
        "grade_label": grade_label,
        "penalty_detail": {
            "P0": {"count": p0_count, "penalty": p0_penalty},
            "P1": {"count": p1_count, "penalty": p1_penalty},
            "P2": {"count": p2_count, "penalty": p2_penalty},
        }
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="计算知识库健康度")
    parser.add_argument("--p0", type=int, default=0, help="P0问题数量")
    parser.add_argument("--p1", type=int, default=0, help="P1问题数量")
    parser.add_argument("--p2", type=int, default=0, help="P2问题数量")
    
    args = parser.parse_args()
    result = calculate_health(args.p0, args.p1, args.p2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
