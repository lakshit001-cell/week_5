---
name: codestyle
description: >
  Analyzes codebase for stylistic best practices, including variable naming conventions, spacing, inline comments, and docstrings. Use when the user asks to review code quality, check style, clean up files, or lint the code.
---

# Code Style & Quality Verification Workflow

1. **Identify Target Files:**
   Use the `list_files` tool to locate the specific scripts or directories the user wants to review. If none are specified, ask the user which files to evaluate.

2. **Automated Linting:**
   Attempt to run standard linting tools using `run_command` (e.g., `flake8 target_file.py`, `pylint target_file.py` for Python, or `clang-format -n` for C++). 
   **CRITICAL:** Capture the terminal output. If the tool fails because the linter is not installed (e.g., `command not found`), do not halt. Acknowledge the missing tool and proceed to Step 3.

3. **Manual Static Analysis:**
   Use the `read_file` tool to ingest the target code into context. Analyze the code against the following strict criteria:
   - **Naming Conventions:** Ensure variables and functions follow language-standard conventions (e.g., `snake_case` for variables/functions, `PascalCase` for classes). Flag vague, non-descriptive names (like `x`, `data`, `temp`, or `obj`).
   - **Spacing & Formatting:** Check for consistent indentation, trailing whitespace, appropriate line length, and blank lines separating logical blocks and function definitions.
   - **Documentation:** Verify the presence of clear module-level docstrings, well-documented function signatures (args and return types), and inline comments that explain *why* complex logic exists, rather than just stating *what* it does.
   - **Dead Code:** Identify commented-out code blocks or unused imports/variables that clutter the file.
   - **Redundant code** Identify if any redundant code is present in the file and tell the user about it along with line numbers.

4. **Generate Style Report:**
   Output a structured markdown report to the user containing:
   - An overall assessment of the code's readability.
   - A bulleted list of specific violations, citing exact line numbers and the offending code snippets.
   - Concrete recommendations for how to rewrite those lines.

5. **Apply Fixes (Requires Permission):**
   Ask the user if they would like you to automatically refactor the file to fix the flagged issues. If they approve, use the `edit_file` tool to apply the spacing, naming, and comment updates. 

6. **Safety Verification (Post-Edit):**
   If fixes were applied in Step 5, use `run_command` to execute the project's test suite (e.g., `pytest` or a compilation check). **CRITICAL:** You must verify that your stylistic changes (like renaming a variable) did not accidentally break the underlying logic or create `NameError` exceptions elsewhere in the file.