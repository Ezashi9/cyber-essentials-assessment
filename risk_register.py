"""Validate a 5x5 risk register CSV and turn it into a Markdown report and heat maps.

Usage:
    python risk_register.py [risk_register.csv] [--out output]

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from html import escape
from pathlib import Path

REQUIRED_FIELDS = [
    "id",
    "title",
    "description",
    "likelihood",
    "impact",
    "recommended_control",
    "residual_likelihood",
    "residual_impact",
    "ce_theme",
    "owner",
    "timeframe",
]
SCORE_FIELDS = ["likelihood", "impact", "residual_likelihood", "residual_impact"]

CE_THEMES = {
    "Firewalls",
    "Secure Configuration",
    "Security Update Management",
    "User Access Control",
    "Malware Protection",
    "Outside CE",
}
TEN_STEPS = {
    "Risk management",
    "Engagement and training",
    "Asset management",
    "Architecture and configuration",
    "Vulnerability management",
    "Identity and access management",
    "Data security",
    "Logging and monitoring",
    "Incident management",
    "Supply chain security",
}
TIMEFRAMES = ["Quick win", "3 months", "Longer term"]

LIKELIHOOD_LABELS = {1: "Rare", 2: "Unlikely", 3: "Possible", 4: "Likely", 5: "Almost certain"}
IMPACT_LABELS = {1: "Negligible", 2: "Minor", 3: "Moderate", 4: "Major", 5: "Severe"}

# Score bands: score = likelihood x impact, so possible values run 1 to 25.
RATING_BANDS = [(20, "Critical"), (10, "High"), (5, "Medium"), (1, "Low")]
RATING_COLOURS = {
    "Critical": "#b91c1c",
    "High": "#ea580c",
    "Medium": "#facc15",
    "Low": "#16a34a",
}


class ValidationError(Exception):
    def __init__(self, errors: list[str]):
        super().__init__("\n".join(errors))
        self.errors = errors


@dataclass
class Risk:
    id: str
    title: str
    description: str
    likelihood: int
    impact: int
    recommended_control: str
    residual_likelihood: int
    residual_impact: int
    ce_themes: list[str]
    ten_steps: list[str]
    owner: str
    timeframe: str
    assets: str = ""
    existing_controls: str = ""
    est_cost: str = ""

    @property
    def inherent_score(self) -> int:
        return self.likelihood * self.impact

    @property
    def residual_score(self) -> int:
        return self.residual_likelihood * self.residual_impact

    @property
    def inherent_rating(self) -> str:
        return rating(self.inherent_score)

    @property
    def residual_rating(self) -> str:
        return rating(self.residual_score)


def rating(score: int) -> str:
    if not 1 <= score <= 25:
        raise ValueError(f"score must be 1-25, got {score}")
    for floor, name in RATING_BANDS:
        if score >= floor:
            return name
    raise AssertionError("unreachable")


def split_list(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def _parse_score(row_label: str, field: str, raw: str, errors: list[str]) -> int | None:
    try:
        value = int(raw.strip())
    except ValueError:
        errors.append(f"{row_label}: {field} must be a whole number 1-5, got {raw!r}")
        return None
    if not 1 <= value <= 5:
        errors.append(f"{row_label}: {field} must be 1-5, got {value}")
        return None
    return value


def validate_rows(rows: list[dict[str, str]]) -> list[Risk]:
    """Check every row and return Risk objects, or raise ValidationError listing every problem."""
    errors: list[str] = []
    risks: list[Risk] = []
    seen_ids: set[str] = set()

    if not rows:
        raise ValidationError(["register is empty"])

    missing_columns = [f for f in REQUIRED_FIELDS if f not in rows[0]]
    if missing_columns:
        raise ValidationError([f"missing column(s): {', '.join(missing_columns)}"])

    for line_no, row in enumerate(rows, start=2):
        risk_id = (row.get("id") or "").strip()
        label = f"line {line_no} ({risk_id or 'no id'})"
        row_errors: list[str] = []

        for field in REQUIRED_FIELDS:
            if not (row.get(field) or "").strip():
                row_errors.append(f"{label}: required field '{field}' is empty")

        if risk_id:
            if risk_id in seen_ids:
                row_errors.append(f"{label}: duplicate id {risk_id}")
            seen_ids.add(risk_id)

        scores = {}
        for field in SCORE_FIELDS:
            raw = row.get(field) or ""
            if raw.strip():
                scores[field] = _parse_score(label, field, raw, row_errors)

        themes = split_list(row.get("ce_theme") or "")
        for theme in themes:
            if theme not in CE_THEMES:
                row_errors.append(f"{label}: unknown Cyber Essentials theme {theme!r}")
        if "Outside CE" in themes and len(themes) > 1:
            row_errors.append(f"{label}: 'Outside CE' can't be combined with a CE theme")

        steps = split_list(row.get("ten_steps") or "")
        for step in steps:
            if step not in TEN_STEPS:
                row_errors.append(f"{label}: unknown NCSC 10 Steps area {step!r}")

        timeframe = (row.get("timeframe") or "").strip()
        if timeframe and timeframe not in TIMEFRAMES:
            row_errors.append(f"{label}: timeframe must be one of {TIMEFRAMES}, got {timeframe!r}")

        if not row_errors and all(v is not None for v in scores.values()):
            risk = Risk(
                id=risk_id,
                title=row["title"].strip(),
                description=row["description"].strip(),
                likelihood=scores["likelihood"],
                impact=scores["impact"],
                recommended_control=row["recommended_control"].strip(),
                residual_likelihood=scores["residual_likelihood"],
                residual_impact=scores["residual_impact"],
                ce_themes=themes,
                ten_steps=steps,
                owner=row["owner"].strip(),
                timeframe=timeframe,
                assets=(row.get("assets") or "").strip(),
                existing_controls=(row.get("existing_controls") or "").strip(),
                est_cost=(row.get("est_cost") or "").strip(),
            )
            if risk.residual_score > risk.inherent_score:
                row_errors.append(
                    f"{label}: residual score {risk.residual_score} is higher than "
                    f"inherent score {risk.inherent_score}; a control shouldn't raise risk"
                )
            else:
                risks.append(risk)

        errors.extend(row_errors)

    if errors:
        raise ValidationError(errors)
    return risks


def load_register(path: Path) -> list[Risk]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return validate_rows(rows)


def sort_by_priority(risks: list[Risk]) -> list[Risk]:
    """Highest inherent score first; ties broken by impact, then id."""
    return sorted(risks, key=lambda r: (-r.inherent_score, -r.impact, r.id))


def _md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown(risks: list[Risk]) -> str:
    ordered = sort_by_priority(risks)
    lines = [
        "# Risk register",
        "",
        "Generated by `risk_register.py` from `risk_register.csv`. Do not edit by hand.",
        "",
        "Score = likelihood x impact (each 1-5). "
        "Ratings: Critical 20-25, High 10-16, Medium 5-9, Low 1-4.",
        "",
        "## Summary",
        "",
        "| Rating | Inherent | Residual |",
        "|---|---|---|",
    ]
    for _, name in RATING_BANDS:
        inherent = sum(1 for r in risks if r.inherent_rating == name)
        residual = sum(1 for r in risks if r.residual_rating == name)
        lines.append(f"| {name} | {inherent} | {residual} |")
    total_in = sum(r.inherent_score for r in risks)
    total_res = sum(r.residual_score for r in risks)
    reduction = round(100 * (total_in - total_res) / total_in) if total_in else 0
    lines += [
        "",
        f"Total score across all {len(risks)} risks falls from {total_in} to {total_res} "
        f"({reduction}% lower) if every recommended control is put in place.",
        "",
        "## Risks, highest first",
        "",
        "| ID | Risk | L | I | Inherent | Recommended control | L | I | Residual | Cyber Essentials | When |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in ordered:
        lines.append(
            f"| {r.id} | {_md(r.title)} | {r.likelihood} | {r.impact} | "
            f"**{r.inherent_score} {r.inherent_rating}** | {_md(r.recommended_control)} | "
            f"{r.residual_likelihood} | {r.residual_impact} | "
            f"{r.residual_score} {r.residual_rating} | {_md(', '.join(r.ce_themes))} | {r.timeframe} |"
        )
    lines += [
        "",
        "L = likelihood, I = impact. The first L and I are before the control, the second pair after.",
        "",
        "## Detail",
        "",
    ]
    for r in ordered:
        lines += [
            f"### {r.id}: {r.title}",
            "",
            r.description,
            "",
            "| | |",
            "|---|---|",
            f"| Assets | {_md(r.assets) or 'n/a'} |",
            f"| Existing controls | {_md(r.existing_controls) or 'n/a'} |",
            f"| Inherent | {LIKELIHOOD_LABELS[r.likelihood]} ({r.likelihood}) x "
            f"{IMPACT_LABELS[r.impact]} ({r.impact}) = **{r.inherent_score} {r.inherent_rating}** |",
            f"| Recommended control | {_md(r.recommended_control)} |",
            f"| Residual | {LIKELIHOOD_LABELS[r.residual_likelihood]} ({r.residual_likelihood}) x "
            f"{IMPACT_LABELS[r.residual_impact]} ({r.residual_impact}) = "
            f"**{r.residual_score} {r.residual_rating}** |",
            f"| Cyber Essentials theme | {_md(', '.join(r.ce_themes))} |",
            f"| NCSC 10 Steps | {_md(', '.join(r.ten_steps)) or 'n/a'} |",
            f"| Owner | {_md(r.owner)} |",
            f"| Timeframe | {r.timeframe} |",
            f"| Rough cost | {_md(r.est_cost) or 'n/a'} |",
            "",
        ]
    return "\n".join(lines)


def heatmap_grid(risks: list[Risk], residual: bool = False) -> dict[tuple[int, int], list[str]]:
    """Map (likelihood, impact) -> risk ids in that cell."""
    grid: dict[tuple[int, int], list[str]] = {
        (l, i): [] for l in range(1, 6) for i in range(1, 6)
    }
    for r in sort_by_priority(risks):
        key = (r.residual_likelihood, r.residual_impact) if residual else (r.likelihood, r.impact)
        grid[key].append(r.id)
    return grid


def render_ascii_heatmap(risks: list[Risk], residual: bool = False) -> str:
    grid = heatmap_grid(risks, residual)
    width = max(9, max(len(",".join(ids)) for ids in grid.values()) + 2)
    title = "Residual risk (after controls)" if residual else "Inherent risk (before controls)"
    sep = "      +" + ("-" * width + "+") * 5
    out = [title, "", "Likelihood"]
    for l in range(5, 0, -1):
        out.append(sep)
        cells = []
        for i in range(1, 6):
            ids = grid[(l, i)]
            text = ",".join(ids) if ids else f"({rating(l * i)[0]})"
            cells.append(text.center(width))
        out.append(f"  {l}   |" + "|".join(cells) + "|")
    out.append(sep)
    out.append("       " + "".join(str(i).center(width + 1) for i in range(1, 6)))
    out.append("       " + "Impact".center((width + 1) * 5))
    out.append("")
    out.append("Empty cells show their rating band: (C)ritical, (H)igh, (M)edium, (L)ow.")
    return "\n".join(out)


def render_svg_heatmap(risks: list[Risk], residual: bool = False) -> str:
    grid = heatmap_grid(risks, residual)
    cell, left, top = 110, 120, 60
    width, height = left + cell * 5 + 20, top + cell * 5 + 90
    title = "Residual risk (after controls)" if residual else "Inherent risk (before controls)"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Segoe UI, Arial, sans-serif" role="img">',
        f"<title>{escape(title)}</title>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="32" text-anchor="middle" font-size="20" '
        f'font-weight="600" fill="#111827">{escape(title)}</text>',
    ]
    for l in range(1, 6):
        y = top + (5 - l) * cell
        for i in range(1, 6):
            x = left + (i - 1) * cell
            band = rating(l * i)
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'fill="{RATING_COLOURS[band]}" fill-opacity="0.35" stroke="#ffffff" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{x + 6}" y="{y + 16}" font-size="11" fill="#374151">'
                f"{l * i} {band}</text>"
            )
            ids = grid[(l, i)]
            for n, start in enumerate(range(0, len(ids), 3)):
                chunk = ", ".join(ids[start:start + 3])
                parts.append(
                    f'<text x="{x + cell / 2}" y="{y + 52 + n * 18}" text-anchor="middle" '
                    f'font-size="14" font-weight="700" fill="#111827">{escape(chunk)}</text>'
                )
        parts.append(
            f'<text x="{left - 10}" y="{y + cell / 2 + 4}" text-anchor="end" font-size="12" '
            f'fill="#111827">{l} {LIKELIHOOD_LABELS[l]}</text>'
        )
    for i in range(1, 6):
        x = left + (i - 1) * cell + cell / 2
        parts.append(
            f'<text x="{x}" y="{top + cell * 5 + 20}" text-anchor="middle" font-size="12" '
            f'fill="#111827">{i} {IMPACT_LABELS[i]}</text>'
        )
    parts.append(
        f'<text x="{left + cell * 2.5}" y="{top + cell * 5 + 50}" text-anchor="middle" '
        f'font-size="14" font-weight="600" fill="#111827">Impact</text>'
    )
    parts.append(
        f'<text x="20" y="{top + cell * 2.5}" text-anchor="middle" font-size="14" font-weight="600" '
        f'fill="#111827" transform="rotate(-90 20 {top + cell * 2.5})">Likelihood</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_outputs(risks: list[Risk], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "risk_register.md": render_markdown(risks) + "\n",
        "heatmap.txt": render_ascii_heatmap(risks) + "\n\n\n" + render_ascii_heatmap(risks, residual=True) + "\n",
        "heatmap_inherent.svg": render_svg_heatmap(risks),
        "heatmap_residual.svg": render_svg_heatmap(risks, residual=True),
    }
    written = []
    for name, content in files.items():
        path = out_dir / name
        path.write_text(content, encoding="utf-8", newline="\n")
        written.append(path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv", nargs="?", default="risk_register.csv", type=Path)
    parser.add_argument("--out", default="output", type=Path, help="output folder (default: output)")
    args = parser.parse_args(argv)

    try:
        risks = load_register(args.csv)
    except FileNotFoundError:
        print(f"error: {args.csv} not found", file=sys.stderr)
        return 2
    except ValidationError as exc:
        print(f"{args.csv} failed validation ({len(exc.errors)} problem(s)):", file=sys.stderr)
        for err in exc.errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    written = write_outputs(risks, args.out)
    print(f"{len(risks)} risks validated.")
    print(render_ascii_heatmap(risks))
    print()
    for path in written:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
