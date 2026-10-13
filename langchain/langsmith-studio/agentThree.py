from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage

@tool
def read_email(runtime: ToolRuntime) -> str:
    """Read an email from the given address."""
    # take email from state
    return runtime.state["email"]

@tool
def load_emails_to_inbox(runtime: ToolRuntime) -> Command:
    """Refresh the inbox from the given address."""
    return Command(update={
        "email": "Hi Seán, I'm going to be late for our meeting tomorrow. Can we reschedule? Best, John.",
        "messages": [ToolMessage("Successfully loaded emails.", tool_call_id=runtime.tool_call_id)]}
        )


@tool
def send_email(body: str) -> str:
    """Send an email to the given address with the given subject and body."""
    # fake email sending
    return f"Email sent"

from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import HumanInTheLoopMiddleware

class EmailState(AgentState):
    email: str

agent = create_agent(
    model="gpt-5-nano",
    tools=[read_email, load_emails_to_inbox, send_email],
    state_schema=EmailState,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "read_email": False,
                "send_email": True,
            },
            description_prefix="Tool execution requires approval",
        ),
    ],
    system_prompt="Always load_emails before read."
)
