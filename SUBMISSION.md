**Instructions**
1.Use standard commands to run from week_5/project directory.
```text
pip install openai python-dotenv requests markdownify trafilatura textual
```
This week work builds upon week 4 code.  Two new skills are added on top of week 4 namely commit+push and codestyle.

**Commit** : This skill allows the agent to run the test suite, verify results and then commit the code and push it to a remote repositry on its own. It simulates a real testing enviroment where users test the code, fix any bugs and then commit the code back to github.

**CODESTYLE**: This skills allows the agent to analyse the code by running lint tools. Additionaly it also performs analysis itsels by using week 3 tools of read_file and idenfitifes case issues, redundant code, commented out portion, formatting etc. After this it gives a detailed report to the user highlighting all the issues and also giving line numbers and asking user permission to fix those errors.
While fixing such errors the agent is strictly prompted to make sure that making changes do not lead to failure in test cases.

To run this skills just write execute <skill name> and the agent will pick up from there.

The agent testing was done on python request library along with additional handwritten code. It was able to connect to mcp servers of git and execute commit and push commands and was also able to identify code style issues and resolve them without breaking the code.