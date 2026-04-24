club_list_response = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "count": {"type": "integer"},
        "next": {"type": ["string", "null"]},
        "previous": {"type": ["string", "null"]},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "bookTitle": {"type": "string"},
                    "bookAuthors": {"type": "string"},
                    "publicationYear": {"type": "integer"},
                    "description": {"type": "string"},
                    "telegramChatLink": {"type": "string"},
                    "owner": {"type": "integer"},
                    "members": {
                        "type": "array",
                        "items": {"type": "integer"}
                    },
                    "reviews": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "club": {"type": "integer"},
                                "user": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "username": {"type": "string"}
                                    },
                                    "required": ["id", "username"]
                                },
                                "review": {"type": "string"},
                                "assessment": {"type": "integer"},
                                "readPages": {"type": "integer"},
                                "created": {"type": "string"},
                                "modified": {"type": ["string", "null"]}
                            },
                            "required": ["id", "club", "user", "review", "assessment", "readPages", "created"]
                        }
                    }
                },
                "required": ["id", "bookTitle", "bookAuthors", "publicationYear", "telegramChatLink", "owner", "members"]
            }
        }
    },
    "required": ["count", "next", "previous", "results"]
}
