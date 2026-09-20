from agent.services import Thread
from agent.models import ThreadConfig
from agent.errors import GetThreadError

async def get_thread(thread_config: ThreadConfig):
    try:
        return Thread.from_config(thread_config)
    except Exception as e:
        raise GetThreadError(str(e))

