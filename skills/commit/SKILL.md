---
name: commit
description: >
  Stage changes and write a clean conventional-commit message. Use when the
  user asks to commit, save work, or "wrap this up" — not for pushing or PRs.
---

# Automated Commit Workflow

1. **Safety Check (Test Suite):**
   Run the project's test suite using `run_command`. If the tests fail, STOP immediately. Do not commit broken code. Report the failure to the user.
   
2. **Review Changes:**
   Run `git status` and `git diff --staged` (or `git diff` if nothing is staged) to analyze exactly what has been modified.
   
3. **Stage the Files:**
   Ask the user for explicit permission before running `git add -A` or staging specific files.
   
4. **Draft the Commit Message:**
   Write a strict conventional-commit message using the format: `type(scope): summary`. 
   - Ensure the mood is imperative (e.g., "add", not "added").
   - Keep the summary under 72 characters.
   
5. **Final Execution & Verification:**
   Show the user the proposed commit message and the list of files to be committed. Once the user approves, execute the `git commit -m "..."` command using `run_command`. 
   **CRITICAL:** You MUST read the terminal output of the commit command. If it contains errors like "fatal: not a git repository", you must stop, report the exact error to the user, and explain that the commit failed. Do not claim success unless the command returns a clean exit code.