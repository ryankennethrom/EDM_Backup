from templates import Config
from utils.dir_utils import pick_folder
from utils.config_utils import get_config
import textoutputcontroller as toc
from .registry import register
import ast
import os
import fnmatch
import re
import os

def match_pattern(pattern: dict, subject: str) -> bool:
    value = subject
    pat = pattern["pattern"]

    case_sensitive = pattern.get("case_sensitive", False)
    predicate = pattern.get("predicate", "contains")
    match_mode = pattern.get("match_mode", "literal")
    negated = pattern.get("negated", False)

    if not case_sensitive:
        value = value.lower()
        pat = pat.lower()

    result = False

    # -------- literal --------
    if match_mode == "literal":
        if predicate == "contains":
            result = pat in value
        elif predicate == "startswith":
            result = value.startswith(pat)
        elif predicate == "endswith":
            result = value.endswith(pat)
        elif predicate == "equals":
            result = value == pat
        else:
            raise ValueError(f"Unknown predicate: {predicate}")

    # -------- wildcard --------
    elif match_mode == "wildcard":
        result = fnmatch.fnmatch(value, pat)

    # -------- regex --------
    elif match_mode == "regex":
        flags = 0 if case_sensitive else re.IGNORECASE
        result = re.search(pat, value, flags) is not None

    else:
        raise ValueError(f"Unknown match_mode: {match_mode}")

    if negated:
        result = not result

    return result

@register
class PatternDestinationConfig(Config):
    def get_settings_description(self):
        return "Backup files into specific destination folders if certain patterns exist in the filename ?"

    def get_value_pretty(self):
        value = self.get_config_value()
        if value:
            try:
                destinations = ast.literal_eval(value)
            except Exception:
                print("Invalid previous config, resetting.")
                destinations = []
        else:
            destinations = []
        out = "\n\n"
        for i, d in enumerate(destinations):
            patterns = d["patterns"]

            out += f"   [{i+1}] Put file in {d["destination_directory"]}\n"

            for i, p in enumerate(patterns):
                out += (
                    f"      <{i + 1}> "
                    f"if file {p.get('predicate')} '{p.get('pattern')}' | "
                    f"match_mode={p.get('match_mode', 'literal')} | "
                    f"case_sensitive={'yes' if p.get('case_sensitive') else 'no'} | "
                    f"negated={'yes' if p.get('negated') else 'no'} \n"
                )
        return out

        

    def prompt(self, prev_config_value):
        if prev_config_value:
            try:
                destinations = ast.literal_eval(prev_config_value)
            except Exception:
                print("Invalid previous config, resetting.")
                destinations = []
        else:
            destinations = []
        
        while True:
            print("\n=== Pattern --> Destination Rules ===\n")

            for i, d in enumerate(destinations):
                print(f"{i+1}. {d['destination_directory']} "
                      f"(patterns={len(d.get('patterns', []))})")

            print("\nA) Add destination")
            print("E) Edit destination")
            print("D) Delete destination")
            print("Q) Done")

            choice = input("Select option: ").strip().lower()

            if choice == "q":
                break

            # ---------------- add destination ----------------
            if choice == "a":
                folder = pick_folder("Select destination directory")
                if not folder:
                    continue

                destinations.append({
                    "destination_directory": folder,
                    "patterns": []
                })

            # ---------------- edit destination ----------------
            elif choice == "e":
                idx = input("Destination number: ").strip()
                if not idx.isdigit():
                    continue

                dest = destinations[int(idx) - 1]

                while True:
                    print(f"\nEditing: {dest['destination_directory']}\n")

                    patterns = dest["patterns"]

                    for i, p in enumerate(patterns):
                        print(
                            f"{i + 1}. "
                            f"{p.get('predicate')} '{p.get('pattern')}' | "
                            f"mode={p.get('match_mode', 'literal')} | "
                            f"case={'yes' if p.get('case_sensitive') else 'no'} | "
                            f"negated={'yes' if p.get('negated') else 'no'}"
                        )

                    print("\nA) Add pattern")
                    print("D) Delete pattern")
                    print("B) Back")

                    sub = input("Select option: ").strip().lower()

                    if sub == "b":
                        break

                    # ---------- add pattern ----------
                    if sub == "a":
                        patterns.append({
                            "pattern": input("Pattern: ").strip(),
                            "predicate": input(
                                "Predicate (contains/startswith/endswith/equals) [contains]: "
                            ).strip().lower() or "contains",
                            "match_mode": input(
                                "Match mode (literal/wildcard/regex) [literal]: "
                            ).strip().lower() or "literal",
                            "case_sensitive": input("Case sensitive? (y/N): ").lower() == "y",
                            "negated": input("Negated? (y/N): ").lower() == "y",
                        })

                    # ---------- delete pattern ----------
                    elif sub == "d":
                        pidx = input("Pattern number: ").strip()
                        if pidx.isdigit():
                            pidx = int(pidx) - 1
                            if 0 <= pidx < len(patterns):
                                patterns.pop(pidx)

            # ---------------- delete destination ----------------
            elif choice == "d":
                idx = input("Destination number: ").strip()
                if idx.isdigit():
                    idx = int(idx) - 1
                    if 0 <= idx < len(destinations):
                        destinations.pop(idx)

        return str(destinations)

    def resolve_helper(self, resolve_params):
        src_filename = resolve_params.src_filename
        
        destinations = ast.literal_eval(self.config_value)

        for dest in destinations:
            patterns = dest.get("patterns", [])

            for p in patterns:
                if match_pattern(p, src_filename):
                    return dest["destination_directory"]
        return resolve_params.dst_dirpath


