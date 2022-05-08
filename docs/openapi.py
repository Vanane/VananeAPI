from fastapi.openapi.utils import get_openapi

class SchemaBuilder:
    app:object

    def __init__(self, app):
        self.app = app        
    
    def build(self):
        DOCS_TITLE = "Vanane API"
        DOCS_VERSION = "0.1"
        openapi_schema = get_openapi(
            title=DOCS_TITLE,
            version=DOCS_VERSION,
            routes=self.app.routes,
        )

        openapi_schema["info"] = {
            "title" : DOCS_TITLE,
            "version" : DOCS_VERSION,
            "description" : "Learn about programming language history!",
            "termsOfService": "http://programming-languages.com/terms/",
            "contact": {
            "name": "Get Help with this API",
            "url": "http://www.programming-languages.com/help",
            "email": "support@programming-languages.com"
            },
            "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            },            
        }


        openapi_schema["paths"]["/dice2/{expr}"]["get"]["responses"] = {
            "200": {
                "content": {
                    "application/json": {
                        "example":[[1, 1, 4, 8, 2, 4, 20], [3, 5, 5, 7, 1, 2, 23], [3, 3, 4, 1, 2, 5, 17]],
                        "schema": {
                            "properties":
                            {
                                "dices":{
                                    "title":""
                                }
                            }
                        }
                    }
                }
            },
            "400": {
                "content": {
                    "application/json": {
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



        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema
