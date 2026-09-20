from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.helpers import new_task_from_user_message, get_message_text
from a2a.types import (
    AgentCard,
    Part,
    TaskState,
)
from typing import cast
from langchain_core.messages import HumanMessage, SystemMessage
from agent.backend import get_agent, get_thread, get_system_prompt
from protocol.models import AgentExecutorModel

class Executor(AgentExecutor):

    def __init__(self, agent_executor: AgentExecutorModel):
        self.agent_executor = agent_executor
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:

        self.agent = await get_agent(
            self.agent_executor.llm_config,
            list(self.agent_executor.mcp_servers.all())
        )


        if context.message is None:
            raise ValueError("A message is required to execute the task.")

        if context.context_id is None:
            raise ValueError("A context_id is required to execute the task.")

        user_text = get_message_text(context.message)

        task = (
            context.current_task
            or new_task_from_user_message(context.message)
        )

        await event_queue.enqueue_event(task)
        
        updater = TaskUpdater(event_queue, task.id, context.context_id)

        await updater.update_status(
            TaskState.TASK_STATE_WORKING,
            message = updater.new_agent_message([Part(text="Working on the task.")])
        )

        try:
            thread = await get_thread(
                self.agent_executor.thread_config
            )

            system_message = await get_system_prompt(
                self.agent_executor.system_prompt
            )
            
            thread.append(SystemMessage(system_message))
            thread.append(HumanMessage(user_text))

            response = self.agent.invoke(thread)
            response_text = str(response.content)
            
            await updater.update_status(
                TaskState.TASK_STATE_COMPLETED,
                message = updater.new_agent_message([Part(text=response_text)])
            )
            
        except Exception as e:
            await updater.update_status(
                TaskState.TASK_STATE_FAILED,
                message = updater.new_agent_message([Part(text=str(e))])
            )
            

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass

async def get_request_handler(agent_executor: AgentExecutorModel, agent_card: AgentCard):
    
    return DefaultRequestHandler(
        Executor(
            agent_executor
        ),
        InMemoryTaskStore(),
        agent_card
    )