from fastapi.openapi.utils import get_openapi

class SchemaBuilder:
    app:object

    def __init__(self, app):
        self.app = app        
    
    def build(self):
        DOCS_TITLE = "Vanane API"
        DOCS_VERSION = "1.0"
        openapi_schema = get_openapi(
            title=DOCS_TITLE,
            version=DOCS_VERSION,
            routes=self.app.routes,
        )

        # Remove auto-generated default docs
        # Remove the autodoc for / endpoint
        openapi_schema["paths"].pop("/")
        # Remove the autodoc for schemas
        openapi_schema["components"]["schemas"].pop("HTTPValidationError")
        openapi_schema["components"]["schemas"].pop("ValidationError")

        openapi_schema["info"] = {
            "title" : DOCS_TITLE,
            "version" : DOCS_VERSION,
            "description" : "Vanane's API for doing  stuff",
            "contact": {
                "name": "Source code",
                "url": "https://github.com/Vanane/VananeAPI"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            },            
        }


        # Change the description for /dice2/{expr} endpoint
        openapi_schema["paths"]["/dice2/{expr}"]["get"]["summary"] = "Simple dice parser that accept several formats, and returns arrays of results"
        openapi_schema["paths"]["/dice2/{expr}"]["get"]["description"] =\
            "Launches dices or series of dices\nAccepted formats :\
            \n- *dice* : [0-9]+ d [0-9]+\
            \n- *dice with bonus* : *dice* +|- [0-9]+\
            \n- *expr* : [0-9]+ ( *expr* )\
            "
        # Change the response formats for /dice2/{expr} endpoint
        openapi_schema["paths"]["/dice2/{expr}"]["get"]["responses"] = {
            "200": {
                "content": {
                    "application/json": {
                        "example":[[1, 1, 4, 8, 14], [3, 5, 5, 7, 20], [3, 3, 4, 1, 11]],
                        "schema": {
                            "$ref":"#/components/schemas/DiceResult"
                        }
                    }
                }
            },
            "400": {
                "content": {
                    "application/json": {
                        "example":{
                            "error":"syntax"
                        },
                        "schema": {
                            "properties": {
                                "error": {
                                    "reason": "Error",
                                    "type": "string",
                                }
                            }
                        }
                    }
                }
            }
        }


        openapi_schema["components"]["schemas"]["DiceResult"] = {
            "title":"DiceResult",
            "type": "array",
            "items": {
                "oneOf": [
                    { "type":"#/components/schemas/DiceResult" },
                    { "type":"int" },
                ]
            }
        }
 

        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema
