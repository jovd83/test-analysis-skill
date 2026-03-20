import argparse
import json
import sys

IMPACT_SCALE = {
    1: "Very Low",
    2: "Low",
    4: "Moderate",
    8: "High",
    16: "Severe",
}

LIKELIHOOD_SCALE = {
    1: "Rare",
    2: "Unlikely",
    3: "Possible",
    4: "Likely",
    5: "Almost Certain",
}


def validate_scale(value: int, allowed: dict[int, str], field_name: str) -> int:
    if value not in allowed:
        allowed_values = ", ".join(str(item) for item in allowed)
        raise ValueError(f"{field_name} must be one of: {allowed_values}")
    return value


def categorize_risk(score: int) -> str:
    if score <= 4:
        return "Low"
    if score <= 12:
        return "Medium"
    if score <= 32:
        return "High"
    return "Critical"


def build_result(impact: int, likelihood: int) -> dict[str, object]:
    impact = validate_scale(impact, IMPACT_SCALE, "impact")
    likelihood = validate_scale(likelihood, LIKELIHOOD_SCALE, "likelihood")
    score = impact * likelihood
    return {
        "impact": impact,
        "impact_label": IMPACT_SCALE[impact],
        "likelihood": likelihood,
        "likelihood_label": LIKELIHOOD_SCALE[likelihood],
        "score": score,
        "category": categorize_risk(score),
        "matrix_position": {
            "impact": impact,
            "likelihood": likelihood,
        },
    }


def format_text(label: str | None, inherent: dict[str, object], residual: dict[str, object] | None) -> str:
    lines = []
    if label:
        lines.append(f"Risk: {label}")
    lines.extend(
        [
            "Inherent Risk:",
            f"  Impact: {inherent['impact']} ({inherent['impact_label']})",
            f"  Likelihood: {inherent['likelihood']} ({inherent['likelihood_label']})",
            f"  Score: {inherent['score']}",
            f"  Category: {inherent['category']}",
        ]
    )
    if residual:
        lines.extend(
            [
                "Residual Risk:",
                f"  Impact: {residual['impact']} ({residual['impact_label']})",
                f"  Likelihood: {residual['likelihood']} ({residual['likelihood_label']})",
                f"  Score: {residual['score']}",
                f"  Category: {residual['category']}",
            ]
        )
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate inherent and optional residual risk using the skill's approved scales."
    )
    parser.add_argument("--impact", type=int, required=True, help="Impact value: 1, 2, 4, 8, or 16")
    parser.add_argument("--likelihood", type=int, required=True, help="Likelihood value: 1 through 5")
    parser.add_argument("--residual-impact", type=int, help="Residual impact after mitigation")
    parser.add_argument("--residual-likelihood", type=int, help="Residual likelihood after mitigation")
    parser.add_argument("--label", help="Optional risk label for text output")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if (args.residual_impact is None) ^ (args.residual_likelihood is None):
        print("Both --residual-impact and --residual-likelihood must be provided together.", file=sys.stderr)
        return 2

    try:
        inherent = build_result(args.impact, args.likelihood)
        residual = None
        if args.residual_impact is not None:
            residual = build_result(args.residual_impact, args.residual_likelihood)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    payload = {
        "label": args.label,
        "inherent": inherent,
        "residual": residual,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(format_text(args.label, inherent, residual))
    return 0


if __name__ == "__main__":
    sys.exit(main())
