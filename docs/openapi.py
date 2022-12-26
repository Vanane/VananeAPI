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

#region Endpoints
        # Change the description for /dice2/{expr} endpoint
        openapi_schema["paths"]["/dice2/{expr}"]["get"]["summary"] = "Simple dice parser"
        openapi_schema["paths"]["/dice2/{expr}"]["get"]["description"] =\
            "Launches dices or series of dices\
            \nAccepted formats :\
            \n- *dice* : [0-9]+ d [0-9]+\
            \n- *dice with bonus* : *dice* +|- [0-9]+\
            \n- *expr* : [0-9]+ ( *expr* )\
            \n\
            \n\n**There are no spaces in the expressions, visible spaces are only for readability.**"
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


        openapi_schema["paths"]["/item"]["get"]["summary"] = "Item generator"
        openapi_schema["paths"]["/item"]["get"]["description"] = ""

        # Change the response formats for /item endpoint
        openapi_schema["paths"]["/item"]["get"]["responses"] = {
            "200": {
                "content": {
                    "application/json": {
                        "example": [{
                                "name": "Mediocre Comically-large Espadon",
                                "modifiers": {
                                "Mediocre": "-50% stat multiplier",
                                "Comically-large": "Hilarously huge",
                                "Espadon": "2d8 of Slash damage"
                                }
                         }],
                        "schema": {
                            "$ref":"#/components/schemas/Item"
                        }
                    }
                }
            }
        }


        openapi_schema["paths"]["/443/auth"]["post"]["summary"] = "Authentication portal"
        openapi_schema["paths"]["/443/auth"]["post"]["description"] =\
            "Provides a temporary JWT, mandatory to use\
            any other endpoint from the 443 category."


        openapi_schema["paths"]["/443/permissions"]["post"]["summary"] = "Permission check"
        openapi_schema["paths"]["/443/permissions"]["post"]["description"] =\
            "Returns a list of all the commands you can or cannot use through the API."

#endregion
        
#region Schemas

        # Schema for a dice result
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

        # Schema for an item
        openapi_schema["components"]["schemas"]["Item"] = {
            "title":"Item",
            "type": "object",
            "properties": {
                "name":{ "type":"string" },
                "modifiers": {
                    "type":"object",
                    "properties": {
                        "ModifierName":{ "type":"string" }
                    }
                },
            }
        }

#endregion
 

        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema
