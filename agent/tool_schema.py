tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": (
                "Search federal documents stored in the database using keywords and agency name. "
                "Use this tool to retrieve real government updates, especially when the user is asking "
                "for recent policies, executive orders, notices, or reports. "
                "Agency names are optional but help improve accuracy when provided (e.g., 'Energy Department', 'Commerce Department')."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Topic or keywords (e.g., 'clean energy', 'AI policies', 'vaccine updates')"
                    },
                    "agency": {
                        "type": "string",
                        "description": "Optional agency name (e.g., 'Energy Department', 'EPA', 'FDA')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of documents to return (default is 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    }
]
