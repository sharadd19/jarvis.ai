from datetime import datetime
import json
from jsonschema import validate, ValidationError
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from backend.MCP.tool_registry import TOOL_REGISTRY
# from openai import AsyncOpenAI
import google.generativeai as genai
from backend.models.AgentInputModel import AgentInput

app = FastAPI()
model = genai.GenerativeModel("gemini-2.0-flash")

# ---------- Models ----------
class AgentRequest(BaseModel):
    prompt: str
    tool_id: str


# ---------- LLM client ----------
# openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def build_agent_prompt(tool):
    today = datetime.now().strftime("%Y-%m-%d")
    return (
         f"You are a smart agent that generates input for a tool selected by the user.\n\n"
        f"Tool name: {tool['name']}\n"
        f"Description: {tool['description']}\n\n"
        f"The tool requires an input object with the following JSON schema:\n"
        f"{json.dumps(tool['input_schema'], indent=2)}\n\n"
        f"Today’s date is {today}.\n"
        f"Given a user request, respond ONLY with a JSON object in this format:\n"
        f'{{"input": {{...}} }}\n\n'
        f"No extra text, no markdown. Example:\n"
        f'{{"input": {{"restaurant": "Dishoom", "datetime": "2025-04-15T19:00:00"}}}}'
    )

async def run_agent(user_prompt: str, tool):
    is_relevant = await tool_is_relevant(user_prompt, tool)
    if not is_relevant:
        return None
    agent_prompt = await build_agent_prompt(tool)
    full_prompt = agent_prompt + "\n\n" + user_prompt
    response = await model.generate_content_async(full_prompt)
    return response.text.strip()

    # response = await openai_client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": agent_prompt},
    #         {"role": "user", "content": user_prompt}
    #     ]
    # )
    # return response.choices[0].message.content.strip()

async def agent_mode(input: AgentInput):
    try:
        tool = TOOL_REGISTRY.get(input.tool)
        if not tool:
            return JSONResponse(status_code=400, content={"error": "Tool does not exist."})

        # Step 1: Ask the LLM how to call the tool
        payload_str = await run_agent(input.message, tool)
        if payload_str is None:
            return JSONResponse(status_code=400, content={"error": "Tool is not relevant to the user prompt."})
        payload = json.loads(payload_str)  # Use json.loads() in production!
        is_valid, error = validate_payload(payload, tool["input_schema"])
        if not is_valid:
            return JSONResponse(status_code=400, content={"error": f"Invalid payload: {error}"})
        # Step 2: Call the MCP server with generated payload
        handler = tool["url"]
        tool_response = handler(payload["input"])
            

        return {
            "generated_input": payload,
            "tool_output": tool_response
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


async def tool_is_relevant(user_prompt, tool):
    user_prompt = (f"You are a smart classifier.\n\n"
        f"User said: '{user_prompt}'\n"
        f"Tool description: {tool['description']}\n"
        f"Is the user trying to do something that this tool should handle? Respond ONLY with 'YES' or 'NO'."
    )
    result = await model.generate_content_async(user_prompt)
    return result.text.strip().lower() == "yes"


def validate_payload(payload, schema):
    try:
        validate(instance=payload["input"], schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)
# # ---------- Route ----------
# @app.post("/agent-mode")
# async def agent_mode(request: AgentRequest):
#     try:
#         tool = TOOL_REGISTRY.get(request.tool_id)
#         if not tool:
#             return JSONResponse(status_code=400, content={"error": "Unknown tool ID"})

#         # Step 1: Ask the LLM how to call the tool
#         payload_str = await run_agent(request.prompt, tool)
#         payload = eval(payload_str)  # Use json.loads() in production!

#         # Step 2: Call the MCP server with generated payload
#         async with httpx.AsyncClient() as client:
#             tool_response = await client.post(
#                 f"{tool['mcp_url']}/mcp/call",
#                 json=payload
#             )

#         return {
#             "generated_input": payload,
#             "tool_output": tool_response.json()
#         }

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})

# # Run with: uvicorn mcp_example_server:app --reload

