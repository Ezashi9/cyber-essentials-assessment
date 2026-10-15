import csv
import io
import tempfile
import unittest
import xml.etree.ElementTree as ET
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import risk_register as rr

PROJECT = Path(__file__).resolve().parent.parent


def make_row(**overrides):
    row = {
        "id": "R99",
        "title": "Test risk",
        "description": "Something bad",
        "assets": "D01",
        "existing_controls": "None",
        "likelihood": "4",
        "impact": "5",
        "recommended_control": "Do the thing",
        "residual_likelihood": "2",
        "residual_impact": "3",
        "ce_theme": "User Access Control",
        "ten_steps": "Identity and access management",
        "owner": "Practice manager",
        "timeframe": "Quick win",
        "est_cost": "£0",
    }
    row.update(overrides)
    return row


class RatingTests(unittest.TestCase):
    def test_band_boundaries(self):
        cases = {1: "Low", 4: "Low", 5: "Medium", 9: "Medium", 10: "High", 16: "High", 20: "Critical", 25: "Critical"}
        for score, expected in cases.items():
            with self.subTest(score=score):
                self.assertEqual(rr.rating(score), expected)

    def test_every_possible_product_has_a_rating(self):
        for l in range(1, 6):
            for i in range(1, 6):
                self.assertIn(rr.rating(l * i), rr.RATING_COLOURS)

    def test_out_of_range_score_rejected(self):
        for bad in (0, 26, -3):
            with self.assertRaises(ValueError):
                rr.rating(bad)


class ValidationTests(unittest.TestCase):
    def test_valid_row_computes_scores(self):
        [risk] = rr.validate_rows([make_row()])
        self.assertEqual(risk.inherent_score, 20)
        self.assertEqual(risk.inherent_rating, "Critical")
        self.assertEqual(risk.residual_score, 6)
        self.assertEqual(risk.residual_rating, "Medium")

    def test_score_out_of_range(self):
        for field in rr.SCORE_FIELDS:
            for bad in ("0", "6"):
                with self.subTest(field=field, value=bad):
                    with self.assertRaises(rr.ValidationError) as ctx:
                        rr.validate_rows([make_row(**{field: bad})])
                    self.assertIn(field, str(ctx.exception))

    def test_non_numeric_score(self):
        with self.assertRaises(rr.ValidationError) as ctx:
            rr.validate_rows([make_row(likelihood="high")])
        self.assertIn("whole number", str(ctx.exception))

    def test_decimal_score_rejected(self):
        with self.assertRaises(rr.ValidationError):
            rr.validate_rows([make_row(impact="3.5")])

    def test_required_field_empty(self):
        for field in rr.REQUIRED_FIELDS:
            with self.subTest(field=field):
                with self.assertRaises(rr.ValidationError) as ctx:
                    rr.validate_rows([make_row(**{field: "  "})])
                self.assertIn(field, str(ctx.exception))

    def test_missing_column(self):
        row = make_row()
        del row["owner"]
        with self.assertRaises(rr.ValidationError) as ctx:
            rr.validate_rows([row])
        self.assertIn("missing column", str(ctx.exception))

    def test_empty_register(self):
        with self.assertRaises(rr.ValidationError):
            rr.validate_rows([])

    def test_duplicate_id(self):
        with self.assertRaises(rr.ValidationError) as ctx:
            rr.validate_rows([make_row(), make_row()])
        self.assertIn("duplicate", str(ctx.exception))

    def test_unknown_ce_theme(self):
        with self.assertRaises(rr.ValidationError) as ctx:
            rr.validate_rows([make_row(ce_theme="Antivirus")])
        self.assertIn("Cyber Essentials theme", str(ctx.exception))

    def test_outside_ce_cannot_mix_with_theme(self):
        with self.assertRaises(rr.ValidationError):
            rr.validate_rows([make_row(ce_theme="Outside CE; Firewalls")])

    def test_multiple_ce_themes_allowed(self):
        [risk] = rr.validate_rows([make_row(ce_theme="Firewalls; Malware Protection")])
        self.assertEqual(risk.ce_themes, ["Firewalls", "Malware Protection"])

    def test_unknown_ten_steps_area(self):
        with self.assertRaises(rr.ValidationError):
            rr.validate_rows([make_row(ten_steps="Cloud security")])

    def test_bad_timeframe(self):
        with self.assertRaises(rr.ValidationError):
            rr.validate_rows([make_row(timeframe="Someday")])

    def test_residual_higher_than_inherent_rejected(self):
        with self.assertRaises(rr.ValidationError) as ctx:
            rr.validate_rows([make_row(likelihood="2", impact="2", residual_likelihood="3", residual_impact="3")])
        self.assertIn("higher than", str(ctx.exception))

    def test_all_errors_reported_together(self):
        rows = [make_row(id="R1", likelihood="9"), make_row(id="R2", owner="")]
        with self.assertRaises(rr.ValidationError) as ctx:
            rr.validate_rows(rows)
        self.assertEqual(len(ctx.exception.errors), 2)
        self.assertIn("line 2", ctx.exception.errors[0])
        self.assertIn("line 3", ctx.exception.errors[1])


class OutputTests(unittest.TestCase):
    def setUp(self):
        self.risks = rr.validate_rows(
            [
                make_row(id="R01", likelihood="5", impact="5", residual_likelihood="1", residual_impact="2"),
                make_row(id="R02", likelihood="3", impact="5", residual_likelihood="2", residual_impact="2"),
                make_row(id="R03", likelihood="5", impact="3", residual_likelihood="1", residual_impact="2"),
                make_row(id="R04", likelihood="1", impact="1", residual_likelihood="1", residual_impact="1"),
            ]
        )

    def test_sort_by_score_then_impact(self):
        ids = [r.id for r in rr.sort_by_priority(self.risks)]
        self.assertEqual(ids, ["R01", "R02", "R03", "R04"])

    def test_heatmap_grid_places_each_risk_once(self):
        for residual in (False, True):
            grid = rr.heatmap_grid(self.risks, residual)
            self.assertEqual(len(grid), 25)
            placed = [rid for ids in grid.values() for rid in ids]
            self.assertCountEqual(placed, ["R01", "R02", "R03", "R04"])
        self.assertEqual(rr.heatmap_grid(self.risks)[(5, 5)], ["R01"])
        self.assertEqual(rr.heatmap_grid(self.risks, residual=True)[(1, 2)], ["R01", "R03"])

    def test_markdown_contains_every_risk_and_summary(self):
        md = rr.render_markdown(self.risks)
        for rid in ("R01", "R02", "R03", "R04"):
            self.assertIn(f"| {rid} |", md)
            self.assertIn(f"### {rid}:", md)
        self.assertIn("| Critical | 1 | 0 |", md)
        self.assertIn("**25 Critical**", md)

    def test_markdown_escapes_pipes(self):
        [risk] = rr.validate_rows([make_row(title="A | B")])
        self.assertIn("A \\| B", rr.render_markdown([risk]))

    def test_ascii_heatmap_shape(self):
        text = rr.render_ascii_heatmap(self.risks)
        self.assertIn("R01", text)
        rows = [line for line in text.splitlines() if line.strip()[:1].isdigit() and "|" in line]
        self.assertEqual(len(rows), 5)
        self.assertTrue(rows[0].strip().startswith("5"))

    def test_svg_is_well_formed(self):
        for residual in (False, True):
            svg = rr.render_svg_heatmap(self.risks, residual)
            root = ET.fromstring(svg)
            self.assertTrue(root.tag.endswith("svg"))
            rects = root.findall("{http://www.w3.org/2000/svg}rect")
            self.assertEqual(len(rects), 26)  # background + 25 cells

    def test_write_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            written = rr.write_outputs(self.risks, Path(tmp) / "out")
            self.assertEqual({p.name for p in written},
                             {"risk_register.md", "heatmap.txt", "heatmap_inherent.svg", "heatmap_residual.svg"})
            for p in written:
                self.assertGreater(p.stat().st_size, 0)


class CliTests(unittest.TestCase):
    def test_bad_csv_exits_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(make_row()))
                writer.writeheader()
                writer.writerow(make_row(impact="7"))
            err = io.StringIO()
            with redirect_stderr(err):
                code = rr.main([str(path), "--out", str(Path(tmp) / "out")])
            self.assertEqual(code, 1)
            self.assertIn("impact must be 1-5", err.getvalue())
            self.assertFalse((Path(tmp) / "out").exists())

    def test_missing_file_exits_2(self):
        with redirect_stderr(io.StringIO()):
            self.assertEqual(rr.main(["does_not_exist.csv"]), 2)


class ProjectRegisterTests(unittest.TestCase):
    """The real register shipped with the assessment must always pass validation."""

    def setUp(self):
        self.risks = rr.load_register(PROJECT / "risk_register.csv")

    def test_loads_and_is_a_sensible_size(self):
        self.assertGreaterEqual(len(self.risks), 12)
        self.assertLessEqual(len(self.risks), 15)

    def test_every_ce_theme_is_covered(self):
        covered = {t for r in self.risks for t in r.ce_themes}
        self.assertTrue(rr.CE_THEMES - {"Outside CE"} <= covered)

    def test_every_risk_maps_to_ten_steps(self):
        for r in self.risks:
            self.assertTrue(r.ten_steps, r.id)

    def test_controls_reduce_every_risk(self):
        for r in self.risks:
            self.assertLess(r.residual_score, r.inherent_score, r.id)

    def test_cli_runs_on_real_register(self):
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stdout(io.StringIO()):
                code = rr.main([str(PROJECT / "risk_register.csv"), "--out", tmp])
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
