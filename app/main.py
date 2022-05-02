from fastapi import FastAPI, APIRouter

from typing import Optional

#[6] [6.1]
RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

# [1] 
app = FastAPI(
    title="Recipe API", 
    openapi_url="/openapi.json"
)

# [2] 
api_router = APIRouter()

#[3] 
@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}

#[7] - New addition, path parameter
# https://fastapi.tiangolo.com/tutorial/path-params/
@api_router.get("/recipe/{recipe_id}", status_code=200) 
def fetch_recipe(*, recipe_id: str) -> dict:  #[8]
    """
    Fetch a single recipe by ID
    """
    print(type(recipe_id)) #[10]

    #[9]
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]
        
#[12]
@api_router.get("/search/", status_code=200) 
def search_recipes( #[13]
    keyword: Optional[str] = None,
    max_results: Optional[int] = 10, #[14][15]
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results based on the max_results query parameter
        return {
            "results": RECIPES[:max_results] #[16]
        }

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES) #[17]
    return {
        "results": list(results)[:max_results]
    }



#[4]
app.include_router(api_router)

#[5]
if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")

# [PART 1]

# [1] We instantiate a FastAPI app object, which is a Python class that provides all the functionality for your API.

#[2] We instantiate an APIRouter which is how we can group our API endpoints (and specify versions and other config which we will look at later)

#[3] By adding the @api_router.get("/", status_code=200) decorator to the root function, we define a basic GET endpoint for our API.

#[4] We use the include_router method of the app object to register the router we created in step 2 on the FastAPI object.

#[5] The __name__ == "__main__" conditional applies when a module is called directly, i.e. if we run python app/main.py. In this scenario, we need to import uvicorn since FastAPI depends on this web server (which we’ll talk more about later)

# [PART 2]

#[6] We’ve created some example recipe data in the RECIPE list of dictionaries. For now, this is basic and minimal but serves our purposes for learning. Later in the tutorial series we will expand this dataset and store it in a database.
#[6.1] We have our toy dataset (later this will go into a database and be expanded)

#[7] We’ve created a new GET endpoint /recipe/{recipe_id}. Here the curly braces indicate the parameter value, which needs to match one of the arguments taken by the endpoint function fetch_recipe.

#[8] The fetch_recipe function defines the logic for the new endpoint. The type hints for the function arguments which match the URL path parameters are used by FastAPI to perform automatic validation and conversion. We’ll look at this in action in a moment.

#[9] We simulate fetching data by ID from a database with a simple list comprehension with an ID conditional check. The data is then serialized and returned as JSON by FastAPI.

#[10] Let’s add a print statement to further understand what’s happening in the endpoint: print(type(recipe_id)) 

#[11] Now change the type hint to a string: def fetch_recipe(*, recipe_id: str) -> dict:

# [PART 3]

#[12] We’ve created a new GET endpoint /search/. Notice it has no path parameters, which we looked at in part 2 (https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-2-url-path-parameters)

#[13] The search_recipes function defines the logic for the new endpoint. Its arguments represent the query parameters to the endpoint. There are two arguments: keyword and max_results. This means that a (local) query with both of these query parameters might look like: http://localhost:8001/search/?keyword=chicken&max_results=2

#[14] Notice that for each argument, we specify its type and default. Both are Optional which comes from the Python standard library typing module. FastAPI is able to use these native Python type declarations to understand that the parameter does not need to be set (if we wanted the parameters to be mandatory, we would omit the Optional)

#[15] Both parameters also have a default, specified via the = sign, for example, the max_result query parameter default is 10. If these parameters are not specified in the request, the default value will be used.

#[16] We implement some basic search functionality using Python list slicing(https://stackoverflow.com/questions/509211/understanding-slice-notation) to limit results

#[17] We use the Python filter capability for a very basic keyword search on our toy dataset. After our search is complete the data is serialized to JSON by the framework.



"""
[LINKS]

[example project repo] = https://github.com/ChristopherGS/ultimate-fastapi-tutorial
[decorator] = https://realpython.com/primer-on-python-decorators/
[OpenAPI Specification] = https://github.com/OAI/OpenAPI-Specification
[JSON Schema] = https://json-schema.org/
[SwaggerUI] = https://github.com/swagger-api/swagger-ui
[ReDoc] = https://github.com/Redocly/redoc
[Python Enhancement Proposal (pep) 484] = https://www.python.org/dev/peps/pep-0484/
[PEP 483] = https://www.python.org/dev/peps/pep-0483/
[Python list slicing] = https://stackoverflow.com/questions/509211/understanding-slice-notation
[typing module] = https://docs.python.org/3/library/typing.html
[tool mypy - useful cheatsheet] = https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""