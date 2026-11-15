import argparse
from app.main import run


def main():
    parser = argparse.ArgumentParser(
        description="Generate and self-evaluate a beginner lesson."
    )
    parser.add_argument(
        "--topic", default="Introduction to RAG",
        help="Topic for the beginner lesson",
    )
    args = parser.parse_args()

    result = run(args.topic)
    print("\n=== EDULOOP AI RESULT ===")
    print("Status:", result.get("status"))
    print("Attempts:", result.get("attempt"))
    print("Run ID:", result.get("run_id"))
    print("Passed:", result.get("passed"))
    print("Lesson saved under outputs/lessons/")
    print("Report saved under outputs/reports/")

    if result.get("evaluation"):
        print("\nRubric:")
        for check in result["evaluation"]["checks"]:
            print(f"{check['check_id']}: {check['status']} - {check['reason']}")


if __name__ == "__main__":
    main()
