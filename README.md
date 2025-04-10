                    [User Interface]
                            |   
          Chat input (text, buttons, mode toggle)
                            |
        -----------------------------------------------
        | Chat Mode                 |  Agent Mode     |
        | (Gemini Flash + OpenAI)   | (Agent + Tools) |
        -----------------------------------------------
                            |
            [Your Backend / Client Runtime]
                            |
            ┌──────────────────────────────┐
            |  Model Router (Gemini, GPT)  |
            └──────────────────────────────┘
                            |
            ┌──────────────────────────────┐
            |  Agent Handler (MCP client)  |
            |  - Detect tool_use           |
            |  - Route to MCP server       |
            |  - Return tool_result        |
            └──────────────────────────────┘
                            |
            ┌──────────────────────────────┐
            |       MCP Server(s)          |
            |  e.g. book_restaurant(),     |
            |       query_calendar(), etc. |
            └──────────────────────────────┘