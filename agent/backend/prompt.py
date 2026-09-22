import re
from agent.models import SystemPrompt, Prompt, Skill
from agent.errors import GetSystemPromptError

skill_pattern = r"\[skill\]\(([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\)"
prompt_pattern = r"\[prompt\]\(([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\)"

def _fetch_prompt(match):
    uuid = match.group(1)
    try:
        prompt = Prompt.objects.get(uuid=uuid)
        return prompt.content
    except:
        return ""
    
def _fetch_skill(match):
    uuid = match.group(1)
    try:
        skill = Skill.objects.get(uuid=uuid)
        return skill.content
    except:
        return ""

async def get_system_prompt(system_prompt: SystemPrompt):
    try:
        prompt = re.sub(prompt_pattern, _fetch_prompt, system_prompt.content)
        prompt = re.sub(skill_pattern, _fetch_skill, prompt)
        return prompt
    except Exception as e:
        raise GetSystemPromptError(str(e))
