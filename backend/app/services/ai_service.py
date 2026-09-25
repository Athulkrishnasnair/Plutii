# Analyse errors
def analyze_error(error: str, code: str = "", context: str = "") -> dict:
    """
    Analyze a developer error.

    This is currently a deterministic mock so that we can
    verify the complete API architecture before connecting
    an external AI provider.
    """

    return {
        "problem": "The application encountered a runtime error.",
        "cause": (
            "The supplied error needs to be inspected together "
            "with the relevant code and execution context."
        ),
        "fix": (
             "Inspect the failing line, verify the values involved, "
            "and make sure the expected data exists before it is used."
        ),
        "verification": [
            "Reproduce the error.",
            "Apply the suggested fix.",
            "Run the affected code again.",
            "Confirm that the original error no longer occurs.",
        ],
    }
