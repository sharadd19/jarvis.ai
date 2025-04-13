# Goals

[x] - Chat endpoint
[x] - Agent endpoint
[x] - Agent handler (MCP Client)
    [x] - Detect tool use
    [x] - Route to MCP server
    [x] - Return tool result
[] - MCP Server
    [x] - Book restaurant
    [x] - If user doesn't provide context for agent, it should not be booking anything. 
        - e.g tell me a story while providing a book_restaurant tool should not work
    [] - Use mcp server api to get list of servers 
    [] - when user clicks on which server, it filters for that one
    [] - sends api call to mcp/status to check its running
    [] - runs that?
[x] - Model router
