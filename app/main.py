"""Run synthetic loan-document verification examples."""

from app.graph import build_graph


def main() -> None:
    graph = build_graph()
    for application_id in ("APP-1001", "APP-1002"):
        result = graph.invoke(
            {"application_id": application_id, "findings": []}
        )
        print("\n" + "=" * 65)
        print(result["final_summary"])
        print("Route:", result["review_route"])
        print("Findings:")
        for finding in result.get("findings", []):
            print(" -", finding)


if __name__ == "__main__":
    main()
