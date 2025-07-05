from src.nali.enums import School

import subprocess
import json
from pathlib import Path


def generate_schools_status(output_path: str = "docs/status.json"):
    results = []

    for school in School:
        school_name = school.name

        try:
            result = subprocess.run(
                ["pytest", "tests", f"--school={school_name}"],
                capture_output=True,
                text=True,
                check=False
            )

            success = result.returncode == 0
            error = None if success else result.stderr + result.stdout

            results.append({
                "school": school_name,
                "status": success,
                "error": None if success else error.strip()
            })

        except Exception as e:
            results.append({
                "school": school_name,
                "status": False,
                "error": str(e)
            })

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    generate_schools_status()
