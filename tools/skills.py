import os
import json

SKILLS_DIR = os.path.abspath(os.environ.get("SKILLS_DIR", "skills"))

def parse_skill_metadata(content):
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            name, desc = "", ""
            for line in frontmatter.split('\n'):
                if line.startswith("name:"): 
                    name = line.split(":", 1)[1].strip()
                if line.startswith("description:"): 
                    desc = line.split(":", 1)[1].strip()
            return name, desc
    return None, None

def get_available_skills_text() -> str:
    if not os.path.exists(SKILLS_DIR):
        return "No skills currently loaded."
    
    metadata = []
    for root, _, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            path = os.path.join(root, "SKILL.md")
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    name, desc = parse_skill_metadata(f.read())
                    if name and desc:
                        metadata.append(f"- **{name}**: {desc}")
            except Exception:
                continue
    
    return "\n".join(metadata) if metadata else "No skills currently loaded."

def load_skill(name: str) -> str:
   
    if not os.path.exists(SKILLS_DIR):
        return json.dumps({"error": "Skills directory not found."})
        
    for root, _, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            path = os.path.join(root, "SKILL.md")
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    skill_name, _ = parse_skill_metadata(content)
                    if skill_name == name:
                        return json.dumps({"content": content})
            except Exception as e:
                return json.dumps({"error": f"Failed to read skill file: {str(e)}"})
                    
    return json.dumps({"error": f"Skill '{name}' not found."})

SKILL_TOOLS = [{
    "type": "function",
    "function": {
        "name": "load_skill",
        "description": "Load the complete instructions and  steps for a given skill procedure.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The exact name string of the skill to fetch."}
            },
            "required": ["name"]
        }
    }
}]