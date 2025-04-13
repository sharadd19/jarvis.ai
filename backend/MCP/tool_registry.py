from backend.MCP.tools.book_restaurant import book_restaurant


TOOL_REGISTRY = {
    "book_restaurant": {
        "name": "Restaurant Booking Tool",
        "description": "Books a table at a restaurant.",
        "url": book_restaurant,
        "input_schema": {
            "type": "object",
            "properties": {
                "restaurant": {"type": "string", "description": "The name of the restaurant"},
                "datetime": {"type": "string", "format": "date-time", "description": "Date and time in ISO format"},
                "party_size": {"type": "integer", "description": "Number of guests"}
            },
            "required": ["restaurant", "datetime"]
        }
        
    },
    "filesystem": {
        "name": "Filesystem Tool",
        "description": "Reads contents of files and folders on disk.",
    }
}