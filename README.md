[WINDOWS]: Run the FastAPI server via poetry with the Python command: `poetry run python app/main.py` Open http://localhost:8001/

## Part 1 Local Setup 

~~~
from fastapi import FastAPI, APIRouter

#[1]
app = FastAPI(title="Recipe API", openapi_url="/openapi.json")
#[2]
api_router = APIRouter()

#[3]
@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}

#[4]
app.include_router(api_router)

#[5]
if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
~~~


1. We instantiate a FastAPI app object, which is a Python class that provides all the functionality for your API.
2. We instantiate an APIRouter which is how we can group our API endpoints (and specify versions and other config which we will look at later)
3. By adding the @api_router.get("/", status_code=200) decorator to the root function, we define a basic GET endpoint for our API.
4. We use the include_router method of the app object to register the router we created in step 2 on the FastAPI object.
5. The __name__ == "__main__" conditional applies when a module is called directly, i.e. if we run python app/main.py. In this scenario, we need to import uvicorn since FastAPI depends on this web server (which we’ll talk more about later)

### Links

<br>

[example project repo](https://github.com/ChristopherGS/ultimate-fastapi-tutorial)

[decorator](https://realpython.com/primer-on-python-decorators/)

[OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification)

[JSON Schema](https://json-schema.org/)

[SwaggerUI](https://github.com/swagger-api/swagger-ui)

[ReDoc](https://github.com/Redocly/redoc)

<br>


## Part 2 Path Parameters 

~~~ 
from fastapi import FastAPI, APIRouter

#[1]
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


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}

#[2]
# New addition, path parameter
# https://fastapi.tiangolo.com/tutorial/path-params/
@api_router.get("/recipe/{recipe_id}", status_code=200)
def fetch_recipe(*, recipe_id: int) -> dict: #[3]
    """
    Fetch a single recipe by ID
    """
    #[4]
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")

~~~ 

1. We’ve created some example recipe data in the RECIPE list of dictionaries. For now, this is basic and minimal but serves our purposes for learning. Later in the tutorial series we will expand this dataset and store it in a database. We have our toy dataset (later this will go into a database and be expanded)
2. We’ve created a new GET endpoint /recipe/{recipe_id}. Here the curly braces indicate the parameter value, which needs to match one of the arguments taken by the endpoint function fetch_recipe.
3. The fetch_recipe function defines the logic for the new endpoint. The type hints for the function arguments which match the URL path parameters are used by FastAPI to perform automatic validation and conversion. We’ll look at this in action in a moment.
4. We simulate fetching data by ID from a database with a simple list comprehension with an ID conditional check. The data is then serialized and returned as JSON by FastAPI.

### Links
<br>

[Python Enhancement Proposal (pep) 484](https://www.python.org/dev/peps/pep-0484/)

[PEP 483](https://www.python.org/dev/peps/pep-0483/)

<br>

## Part 3 Local Setup

~~~
from fastapi import FastAPI, APIRouter

from typing import Optional

#[1]
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


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


@api_router.get("/recipe/{recipe_id}", status_code=200)
def fetch_recipe(*, recipe_id: int) -> dict:
    """
    Fetch a single recipe by ID
    """

    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]

#[2]
# New addition, query parameter
# https://fastapi.tiangolo.com/tutorial/query-params/
@api_router.get("/search/", status_code=200) #[3]
def search_recipes(
    keyword: Optional[str] = None, max_results: Optional[int] = 10 #[4][5]
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECIPES[:max_results]} #[6]

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES) #[7]
    return {"results": list(results)[:max_results]}


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")

~~~

1. We have our toy dataset (later this will go into a database and be expanded)
2. We’ve created a new GET endpoint /search/. Notice it has no path parameters, which we looked at in part 2
3. The search_recipes function defines the logic for the new endpoint. Its arguments represent the query parameters to the endpoint. There are two arguments: keyword and max_results. This means that a (local) query with both of these query parameters might look like: http://localhost:8001/search/?keyword=chicken&max_results=2
4. Notice that for each argument, we specify its type and default. Both are Optional which comes from the Python standard library typing module. FastAPI is able to use these native Python type declarations to understand that the parameter does not need to be set (if we wanted the parameters to be mandatory, we would omit the Optional)
5. Both parameters also have a default, specified via the = sign, for example, the max_result query parameter default is 10. If these parameters are not specified in the request, the default value will be used.
6. We implement some basic search functionality using Python list slicing to limit results.
7. We use the Python filter capability for a very basic keyword search on our toy dataset. After our search is complete the data is serialized to JSON by the framework.

### Links
<br>

[Python list slicing](https://stackoverflow.com/questions/509211/understanding-slice-notation)

[typing module](https://docs.python.org/3/library/typing.html)

[tool mypy - useful cheatsheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

<br>

## Part 4 Pydantic Schemas

### Introduction Pydantic

1. Pydantic describes itself as: `Data validation and settings management using python type annotations`.
2. It's a tool which allows you to be much more precise with your data structures. For example, up until now we have been relying on a dictionary to define a typical recipe in our project. With Pydantic we can define a recipe like this:

~~~
from pydantic import BaseModel

class Recipe(BaseModel):
    id:int
    label: str
    source: str

raw_recipe = {
    'id': 1,
    'label': 'Lasagna',
    'source': 'Grandma Wisdom',
}
structured_recipe = Recipe(**raw_recipe)
print(structured_recipe.id)
~~~
3. In this simple example, the `Recipe` class inherits from the Pydantic `BaseModel`, and we can define each of its expected fields and their types using standard Python type hints.
4. As well as using the `typing`module's `standard types`, you can use Pydantic models recursively like so:

~~~
from pydantic import BaseModel

class Car(BaseModel):
    brand: str
    color: str
    gears: int

class ParkingLot(BaseModel):
    cars: List[Car] # recursively use `Car`
    spaces: int

~~~
5. When you combine these capabilities, you can define very complex objects. This is just scratching the surface of Pydantic's capabilities, here is a quick summary of its benefits:
   - No new micro-language to learn (which means it plays well with IDEs/linters)
   - Great for both "validate this request/response data" and also loading config.
   - Validate complex data structures - Pydantic offers extremely granular `validators`
   - Extensible - you can create custom data types
   - Works with Python data classes
   - It's very fast


<br>

### Pratical Section

<br>

In the `app/main.py` file, you will finds the following new code:
~~~
from app.Schemas import RecipeSearchResults, Recipe, RecipeCreate

#[1] Updated to use a response_model
@api_router.get("/recipe/{recipe_id}",status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> dict:
    """
    Fetch a single recipe by ID
    """
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]
~~~
The `Recipe` response model is imported from a new `schemas.py` file. Let's look the relevant part of the app/schemas.py file:

~~~
from pydantic import BaseModel, HttpUrl

#[2]
class Recipe(BaseModel):
    id: int
    label: str
    source: str
    url: HttpUrl #[3]
~~~
1. Our path parameter endpoint /recipe/{recipe_id}, which we introduced in `part 2` has been updated to include a `response_model` field. Here we define the structure of the JSON response, and we do this via Pydantic.
2. The new `Recipe`class inherits from the pydantic `BaseModel`, and each field is defined with standard type hints...
3. ...except the `url` field, which uses the Pydantic `HttpUrl` helper. This will enforce expected URL components, such as the presence of a scheme (http or https).
<br>
Next, we've updated the search endpoint:

~~~
# app/main.py

from fastapi import FastAPI, APIRouter, Query
from typing import Optional
from app.schemas import RecipeSearchResults

#[1]
@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optinal[str] = Query(None, min_length=3, example="chicken"), #[2]
    max_results: Optinal[int] = 10,
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results base on the max_results query parameter
        return {
            "results": RECIPES[:max_results]
        }
    
    results = filter(lambda recipe: keyword.lower() in recipe["Label"].lower(), RECIPES)
    return {
        "results": list(results)[:max_results]
    }
~~~
<br>

Now let's look at app/schemas.py

<br>

~~~
#[3]
class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe] #[4]
~~~
<br>

1. We've added a responde_model `RecipeSearchResults` to our `/search` endpoint. Notice the response format matches the schema (if it did not, we'd get a Pydantic validation error).
2. We bring in the FastAPI `Query` class, which allows us add additional validation and requirements to our query params,  such as a minimum length. Notice that because we've set the `example` field, this shows up on the docs page when you "Try it".
3. The `RecipesSearchResults` class uses Pudantic's recursive capability to define a field that refers to another Pydantic class we've previously defined, the `Recipe` class. We specify that the `results` field will be a Sequence (which is an iterable with support for `len` and `__getitem__` ) of `Recipes`.

<br>

### Creating a POST endpoint

<br>

Another addition we've made to our API is ability to create new recipes. This is done via a POST request. Here is the updated code in `app/main.py` :
~~~
# New addition, using Pydantic model `RecipeCreate`to define the POST request body
#[1]
@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(
    *,
    recipe_in: RecipeCreate,
) -> dict: #[2]
    """
    Create a new recipe (in memory only)
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )
    RECIPES.append(recipe_entry.dict()) #[3]

    return recipe_entry
~~~
<br>

And here is the updated `app/schemas.py` code:

~~~
#[4]
class RecipeCreate(BaseModel):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int
~~~

<br>
1. To set the function to handle POST requests, we just tweak our `api_router` decorator. Notice that we're also setting the HTTP status_code to 201, since we are creating resources.
2. The `recipe_in` field is the POST request body. By specifying a Pydantic schema, we are able to automatically validate incoming requests, ensuring that their bodies adhere to our schema.
3. To persist the created recipe, we're doing a primitive list append. Naturally, this is just for a toy example and won't persist the data when the server is restarted. Later in the series, we will cover databases.
4. The `RecipeCreate`schema contains a new field, `submitter_id`, so we distinguish it from the `Recipe` schema.

<br>

### Links



[typing module’s standard types](https://pydantic-docs.helpmanual.io/usage/types/#standard-library-types)
[Pydantic offers extremely granular validators](https://pydantic-docs.helpmanual.io/usage/validators/)


## Part 5 Basic Error Handling 

In the `app/main.py` file, you will find the following new code:

~~~
from fastapi import FastAPI, APIRouter, Query, HTTPException #[1]

@api_router.get("/recipe/{recipe_id}", status_code=200, response_module=Recipe)
def fetch_recipe(
    *,
    recipe_id: int
) -> Any:
    """
    Fetch a single recipe by ID
    """

    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not result:
        # The exception is raised, not returned - you wil get a validation erro otherwise.
        #[2]
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with ID {recipe_id} not foud"
        )
    return result[0]
~~~
1. We import the `HTTPException` from FastAPI.
2. Where no recipe is found, we raise an `HTTPExcetion` passing in a `status_code` of 404, which indicates the requested resource has not been found. See `list of HTTP status code`. Notice that we `raise` the exception, we do <strong>not</strong> return it. Returning the exception causes a validation error.

<br>

If you were to set the `recipe_id` to a non-existent one, say 4, then you will get a `Error 404`

> Exercise : 
> 
>   Try POSTing to the `/recipe` endpoint to reate a recipe with the ID 4 and the retry your GET request (you should no longer get a 404). 
> 
> Remember that in our current app's basic form, created entries won't be persisted after you CTRL+C and restart the server.

<br>

### Links

[ list of HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)

<br>

## Part 6 Jinja Templates (Serving HTML int FastAPI) 

<br>

So far in our tutorial series, the only HTML available to view has been the interactive documentation UI which FastAIP offers out of the box. Time now to add a deliberately simple HTML page. We'll code and run ir first (doing beats talking), then further down we'll discuss Jinja2, and what a more realistic approach for serving HTML would be in larger projects.

In the `app/main.py` file, you will find the following new code:

~~~
from fastapi import FastAPI, APIRouter, Query, HTTPException, Resquest
from fastapi.templating import Jinja2Templates

from typing import Optional, Any
from pathlib import Path

from app.schemas import RecipeSearchResults, Recipe, RecipeCreate
from app.recipe_data import RECIPES

#[1]
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()

# Updated to serve a Jinja2 template
# https://www.starlette.io/templates/
# https://jinja.palletsprojects.com/en/3.0.x/templates/#synopsis
@api_router.get("/", status_code=200)
def root(
    request: Request,
) -> dict: #[2]
    """
    Root GET
    """

    #[3]
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "recipes": RECIPES,
        },
    )
~~~

1. We specify our Jinja templates directory by using the standard library `pathlib` module to point to the template's directory's full system path.
2. We've updated the root endpoint, defined in our `root` function. THe function now takes the FastAPI `Request` class as an argument. This is equivalent to `Starlette's Request class` which gives direct and lower-level access to the incoming request.
3. The reason we need access to the request class is that the function now return the FastAPI dedicated `TemplateResponse`. When instantiating this response object, the first argument reqired is the specific tempate file (`index.html` in this case) followeb by a dictionary with the request object and any template variables (in our case, the list of recipes `RECIPES`)

<br>

The other key addition to the example project at this point in the tutorial series is the template itself. This is located in app/templates/index.html

~~~
<!DOCTYPE html>
<html>
    <head>
        <!--1-->
        <link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel ="stylesheet">
    </head>
    
    <body>
        <!-- Skipping for brevity-->
            <!--2-->
                {% for recipe in recipes %}
                    <h2 class="mb-4 font-semibold tracking-widest text-white uppercase title-font>
                        {{recipe.label}}
                    </h2>
                {% endfor %
    </body>
</html>
~~~

> Two key things to highlight from t he (truncated) sample above:

1. The `tailwind CSS library` is used to style the HTML. A full overview of tailwind is beyond the scope of this series, but the quick summary is that HTML element classnames define CSS properties, including things like responsive grid layouts.
2. The Jinja2 tempalte syntax, denoted by the curly brace '{' followed by the percentage sign '%' Here Jinja allows us to loop over the `recipes` variable passed to the template.

> [EXERCISE]
> 
> Use the POST endpoint we added in `part 5`to create a new recipe, and then refresh the home page to see it desplayed.
> 

<br>

### Theory Section - Understanding Jinja Templates

<br>

A templating language allows you to generate HTML/XML or some other markup language with the aid of variables and a constrained amount of programming logic.

The variables and bits of logic are marked with tags, as we saw above with eh loop.

Jinja2 is a popular templating language used by `Flas, Bootle, Pelican` and optionally by `Django`.

Real Python has an excellent `primer on using Jinja`

<br>

### FastAPI and Jinja

<br>

FastAPI is really designed for building API's and microservices. It `can` be used for building web applications that serve HTML using Jinja, but that's not what it is really optimized for.

If you want to build a large website with lots of HTML rendered on ther server, Django is probable a better choice.

However, if you're building a modern website with a frontend framework like React, Angular or Vue, then fetching data from FastAPI is a good fit (we'll be looking at this later in the series).

As a result, in this example series, we're going to use Jinja templates quite sparingly, which is also how they would be used in most real projects. My reasoning for introducing an HTML page at this point in the series is:
    - It will make the example project more engaging. Engaging tutorials are better learning tools.
    - Knowing how to serve ad hoc HTML pages (e.g. for user logins/password confirmation pages) is a common requirement.

<br>

### Links

[ Starlette’s Request class](https://www.starlette.io/requests/)
[tailwind CSS library ](https://tailwindcss.com/)
[Flask](https://github.com/pallets/flask)
[Bottle](https://github.com/bottlepy/bottle)
[Pelican](https://github.com/getpelican/pelican)
[Django](https://github.com/django/django)
[ primer on using Jinja](https://realpython.com/primer-on-jinja-templating/)


<br>

## Part 6b Basic Deployment on Linode 

<br>

### Deploying FastAPI Apps

<br>

This is a serious tutorial design to get you ready to create and deploy a production-ready API. There will be quite a few deployment posts scattered throughout the tutorial, each of which will gradually increase in complexity. We start with the basic version and ratchet complexity later, as we grow stronger and wiser. Later posts will cover:
    - Deploying on Heroku and AWS
    - Doing the deployment in a CI pipeline (best practice)
    - Dockerizing the app
    - Deploying containers
    - Dealing TLS/SSl & custom domains

<br>

### Deployment Options

<br>

Broadly speaking, when you're deciding how to deploy your app you've got two main choices (ignoring running your own hardware, which is more niche these days);
1. A Platform as a Service (PaaS)
2. Smaller Infrastructure as a Service (IaaS)

With a Platform as a Service, all the config is done for you, but you get less control. It tends to be more expensive. With Infrastructure as a Service (IaaS) you have to configure more, but you get a lot of control, and it tends to be cheaper.

In this post, i'll show you how to use Linode for deploying your FastAPI app, in later posts i'll show you how to use other options.

### Linode Free Credit 

### Deployment Step 1: Create Linode Account

### Deployment Step 2: Create VM

### Deployment Step 3: Configure Linode

### Important: Choose the Right Plan

### Deployment Step 4: SSH into your Linode

### Deployment Step 5: Clone the Repo


### Deployment Step 6: Install Some Basics

### Deployment Step 7: Install App Dependencies

### Deployment Step 8: Trigger the Deployment

### Review the Deployment

### Understanding What Happened

### How We Would Improve the Deployment

<br>

### Links

[Linode](https://www.linode.com/)

[this affiliate link you’ll get $100 credit](https://linode.com/christophergs)

[ a primer for ssh](https://frkl.io/blog/ssh-primer/)

[PuTTY](https://www.putty.org/)

[ Makefile](https://opensource.com/article/18/8/what-how-makefile)

[Why do we need both gunicorn and uvicorn? Here’s the relevant snippet from the docs:](https://fastapi.tiangolo.com/deployment/server-workers/)
 uvicorn docs(https://www.uvicorn.org/deployment/#running-behind-nginx)

[Supervisor](http://supervisord.org/running.html)


<br>

## Part 7 Database Setup with SQLAlchemy and Alembic 

<br>

This is the first of the intermediate-level posts. We'll cover quite a lot of ground in this post because there are a lot of parts that all work together and therefore would be more confusing if presented in isolation (because you can't easily spin it up and run it locally without all the parts).

### Theory Section 1 - Quick Introduction to SQLAlchemy

<br>

`SQLAlchemy` is one of the most widely used and highest quality Python third-party libraries. It gives a application developers easy ways to work with relational databases in their Python code.
> `SQLAlchemy` considers the database to be a relational algebra engine, not just a collection of tables. Rows can be selected from not only tables but also joins and other select statements; any of these units can be composed into a larger structure. SQLAlchemy's expression language builds on this concept from its core.

SQLAlchemy is composed of two distinct components:
    - Core - a fully featured SQL abstraction toolkit
    - ORM (Object Relational Mapper) - which is optional

In this tutorial, we will make use of both components, though you can adapt the approach not to use the ORM.

<br>

### Pratical Section 1 - Setting Up Database Tables with SQLAlchemy

<br>

So far in the tutorial, we have not been able to persist data beyond a server restart since all our POST operations just updated data structures in memory. Not we will change that by bringing in a relational database. We'll use `SQLite` because it requires minimal setup so it's useful for learning. With very minor config modifications you can use the same approach for other relational database management systems (RDBMS) such as PostgreeSQL or MySQL.

In the `tutorial repo` open up the part-7 directory. You'll notice that there are a number of new directories compared to previous parts of the tutorial:

~~~
.
├── alembic                    ----> NEW
│  ├── env.py
│  ├── README
│  ├── script.py.mako
│  └── versions
│     └── 238090727082_added_user_and_recipe_tables.py
├── alembic.ini                ----> NEW
├── app
│  ├── __init__.py
│  ├── backend_pre_start.py    ----> NEW
│  ├── crud                    ----> NEW
│  │  ├── __init__.py
│  │  ├── base.py
│  │  ├── crud_recipe.py
│  │  └── crud_user.py
│  ├── db                      ----> NEW
│  │  ├── __init__.py
│  │  ├── base.py
│  │  ├── base_class.py
│  │  ├── init_db.py
│  │  └── session.py
│  ├── deps.py                 ----> NEW
│  ├── initial_data.py
│  ├── main.py
│  ├── models                  ----> NEW
│  │  ├── __init__.py
│  │  ├── recipe.py
│  │  └── user.py
│  ├── recipe_data.py
│  ├── schemas
│  │  ├── __init__.py
│  │  ├── recipe.py
│  │  └── user.py
│  └── templates
│     └── index.html
├── poetry.lock
├── prestart.sh
├── pyproject.toml
├── README.md
└── run.sh
~~~

We'll go through all of these additions in this post, and by the end you'll understand how all the new modules work together to enable not just a one-time database integration, but also migrations as we update our database schemas. More on that soon.

<br>

### FastAPI SQLAlchemy Diagram

<br>

The overall diagram of what we're working towards looks like this:

![SQLAlchemy Diagram](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-7/diagram-overall.jpeg)

<br>

To start off, we will look at the ORM and Data Access Layers:

![ORM and Data Access Layers](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-7/sqlalchemy-diagram-orm.jpeg)

<br>

For now, let's turn our attention to the new `db` directory.

We want to define tables and columns from our Python classes using the ORM. In SQLAlchemy, this is enabled through a `declarative mapping`. The most common pattern is constructing a base class using the SQLAlchemy `declarative_base`  function, and then having all DB model classes inherit from this base class.

We create this base class in the `db/base_class.py` module:

~~~
import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry: t.Dict = {}

@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    #Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

~~~

In other codebases/exxamples you may have seen this done like so:

~~~
Base = declarative_base()
~~~

In our case, we're doing the same thing but with a decorator (provided by SQLAlchemy) so that we can declare some helper methods on our `Base` class - like automatically generating a `__tablename__`.

Having done that, we are now free to define the tables we need for our API. So far we've worked with some toy recipe data stored in memory:

~~~
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
~~~

Therefore the first table we want to define is a `recipe` table that will store the data above. We define this table via the ORM in `models/recipe.py`:

~~~
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Recipe(Base): #[1]
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
    ) #[2]
    label = Column(
        String(256),
        nullable=False,
    )
    url = Column(
        String(256), 
        index=True, 
        nullable=True
    )
    source = Column(
        String(256), 
        nullable=True
    )
    submitter_id = Column(
        String(10), 
        ForeignKey("user.id"), 
        nullable=True,
    ) #[3]
    submitter = relationship(
        "User",
        back_populates="recipes",
    ) #[4]

~~~

Let's break this down:

1. We represent our database `recipe` table with a Python class, which inherits from the `Base` class we defined earlier (this allows SQLAlchemy to detect and map the class to a database table).
2. Every column of the `recipe` table (e.g. `id`,`label`) is defined in the class, setting the column type with SQLAlchemy types like `Integer` and `String`.
3. We define a `one-to-many relationship` between a recipe and user (which we refer to as "submitter"), via the SQLAlchemy `ForeignKey` class.
4. To establish a bidirectional relationship in one-to-many, where the "reverse" side is a many to one, we specify an additional `relationship()` and connect the two using the `relationship.back_populates` parameter.

<br>

As you can infer from the foreign key, we will also need to define a `user` table, since we want to be able to attribute the recipes to users. A user table will set us up for doing auth in later parts of the tutorial.

Our `user` table is defined in `models/user.py`, and follows a similiar structure:

~~~
class User(Base):
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    firt_name = Column(
        String(256),
        nullable=True,
    )
    surname = Column(
        String(256),
        nullable=True,
    )
    email = Column(
        String,
        index=True,
        nullable=False,
    )
    is_superuser = Column(
        Boolean,
        default=False
    )
    recipes = relatioship(
        "Recipe",
        cascade="all, delete-orphan",
        back_populates="submitter",
        uselist=True,
    )
~~~

<br>

Great, we have define our tables. Now what? Well, we haven't yet told SQLAlchemy how to connect to the DB (e.g. what is the database colled, how do we connect to it, what flavor of SQL is it). All this happens in the `SQLAlchemy Engine class`.

We instantiate an engine in the `/db/session.py` module:

~~~
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLACHEMY_DATABSE_URI = "sqlite:///example.db" [#1]

engine = create_engine( #[2]
    SQLACHEMY_DATABASE_URI,
    # required for sqlite
    connect_args = {
        "check_same_thread": False
    },
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine #[4]
)
~~~

<br>

1. The `SQLACHEMY_DATABASE_URI` defines the file where SQLite will persist data.
2. Via the SQLAlchemy `create_engine` function we instantiate our engine, passing in the DB connection URI - note that this connection string can be much more complex and include drivers, dialects, database server locations, users, passwords and ports.
3. The `check_same_thread: False ` config is necessary to work with SQLite - this is a common gotcha because FastAPI can access the database with multiple threads during a single request, so SQLite needs to be configured to allow that.
4. Finally we also create a DB `Session`, which (unlike the engine) is ORM - specific. When working with the ORM, the session object is our main access point to the database.

<br>

From `the SQLAlchemy Session docs:`

> In the most general sense, the Session establishes all conversations with the database and represents a "holding zone" for all the objects which you've loaded or associated with it during its lifespan.

<br>

We are making progress! Next, we will once again turn to Pydantic `which we looked at in part 4` to make it very easy to get our Python code into the right shape for database operations.


<br>

### Pratical Section 2 - Pydantic DB Schemas and CRUD Utilities

<br>

Now let's look at the FastAPI app endpoint logic, specifically the Pydantic DB schemas and CRUD utilities:

![ Pydantic DB schemas and CRUD utilities](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-7/sqlalchemy-pydantic.jpeg)

For those alreadu used to SQLAlchemy and other Python web frameworks like Django or Flask, this part will probably contain something a little different to what you might be used to. Let's zoom in on the diagram:


![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-7/zoomed-pydantic-crud-logic.jpeg)

The key sequencing to understand is that as REST API requests which will require interaction with the database come in, the following occurs:
- The request is routed to the correct path operation (i.e. the function for handling it, such as our `root` function in `main`` py file).
- The relevant Pydantic model is used to validate incoming request data and construct the appropriate data structure to be passed to the CRUD utilities.
- Our CRUD utility functions use a combination of the ORM Session and the shaped data structures to prepare DB queries.

Don’t worry if this isn’t entirely clear yet, we’ll go through each step and by the end of this blog post have brought everything together.

We will create Pydantic models for reading/writing data from our various API endpoints. The terminology can get confusing because we have SQLAlchemy models which look like this

> `name = Column(String)`

and Pydantic models which look like this:

>`name: str`

To help distinguish the two, we tend to keep the Pydantic classes in the `schemas` directory.

Let's look at the `schemas/recipe.py` module:

~~~
from pydantic import BaseModel, HttpUrl
from typing import Sequence

class RecipeBase(BaseModel):
    label: str
    source: str
    url: HttpUrl

class RecipeCreate(RecipeBase):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int

class RecipeUpdate(RecipeBase):
    label: str

# Properties shared by models stored in DB
class RecipeInDBBase(RecipeBase):
    id: int
    submitter_id: int

    class Config:
    orm_module = True

# Properties to return to client
class Recipe(RecipeInDBBase):
    pass

# Properties properties stored in DB
class RecipeInDB(RecipeInDBBase):
    pass
~~~

<br>

Some of these classes, like `Recipe` and `RecipeCreate` existed in previous parts of the tutorial( int the old `schema.py` module), others such as those classes referencing the DB, are new.

Pydantic's `orm_mode` (which you can see in `RecipeInDBBase`) will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes). Without `orm_mode`, if you returned a SQLAlchemy model from your path operation, it wouldn't include the relationship data.

> Why make the distinction between a `Recipe` and `RecipeInDB`? This allows us in future to separate fields which are only relevant for the DB, or which we don't want to return to the client (such as a password field).

As we saw in the diagram, it's not enough to just have the Pydantic schemas. We also need some reusable functions to interact with the database. This will be our data access layer, and by FastAPI convention, these utility classes are defined in the `crud` directory.

These CRUD utility classes help us to do things like:
- Read from a table by ID
- Read from a table by a particular attribute (e.g. by user email)
- Read multiple entries from a table (defining filters and limits)
- Insert new rows into a table
- Delete a row in a table

Each table gets its own CRUD class, which inherits reusable parts from a base class. Let's examine this now in `crud/base.py`.

~~~
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlaclhemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType. UpdateSchemaType]): #[1]
    def __init__(
        self, model: Type[ModelType] #[2]
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

        def get(
            self,
            db: Session,
            id: Any,
        ) -> Optional[ModelType]:
            return db.query(self.model).filter(self.model.id == id).first() #[3]
        
        def get_multi(
            self,
            db: Session,
            *,
            skip: int = 0,
            limit: int = 100,
        ) -> List[ModelType]:
            return db.query(self.model)offset(skip).limit(limit).all() #[4]
        
        def create(
            self, 
            db: Session,
            *,
            obj_in: CreateSchemaType,
        ) -> ModelType:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data) # type: ignore
            db.add(db_obj)
            db.commit() #[5]
            db.refresh(db_obj)
            return db_obj
    )
~~~

<br>

This is one of the trickier bits of code in this part of the tutorial, let's break it down:

1. Models inheriting from `CRUDBase`will be defined with a `SQLAlchemy model` as the firts argument, the the `Pydantic model` (aka schema) for creating and updating rows as the second and third arguments.
2. When instantiating the CRUD class, it expects to be passed the relevant SQLAlchemy model (we'll look at this in a moment).
3. Here are the actual DB queries you have probably been expecting - we use the ORM Session (`db`).query method to chain together different DB queries. These can be as simple or complex as we need. `See the SQLAlchemy documentation on queries`. In this example we filter by ID, allowing us to fetch a single row from the database.
4. Another DB query, this time we fetch multiple database rows by querying and chaining the `.offset` and `.limit` methods, and finishing with `.all()`
5. When creating Db objects, it is necessary to run the session `commit` method (see docs) to complete the row insertion. We'll be looking at tradeoffs to having the commit call here vs. in the endpoint later in the tutorial series (in the Python 3 asyncio and performance blog post).

<br>

Now that we've defined the `CRUDBase` we can use that to define `crud` utilities for each table. The code for these subclasses is much simpler, with the majority of the logic inherited from the base class:

~~~
from app.crud.base import CRUDBase
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate

class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]): #[1]
    ...
recipe = CRUDRecipe(Recipe) #[2]
~~~

<br>

1. The class is defined with the relevant SQLAlchemy `Recipe` model, followed by the Pydantic `RecipeCreate` and `RecipeUpdate` schemas.
2. We instantiate the `CRUDRecipe` class

<br>

Don't worry if this seems a bit abstract at the moment. In the last part of this post, show this being used in the endpoints so can see (and run locally) the API endpoints interacting with the DB, and how the Pydantic schemas and CRUD utilities will work together. However, before we get there, we need to handle the initial creation of the DB, as well as future migrations.


<br>

### Pratical Section 3 - Enabling Migrations with Alembic

<br>

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-7/diagram-alembic.jpeg)

<br>

The goal of this tutorial is to build a production-ready API, and you simply can't setup a database without considering how to make changes to your tables over time. A common solution for this challenge is the `alembic library`, which is designed to work with SQLAlchemy.

Recall our new part-7 file tree:

~~~
.
├── alembic                    ----> NEW
│  ├── env.py
│  ├── README
│  ├── script.py.mako
│  └── versions
│     └── 238090727082_added_user_and_recipe_tables.py
├── alembic.ini                ----> NEW
├── app
...etc.
~~~

The alembic directory contains a few files we'll be using:
- `[ env.py ]` -> where we pass in configuration (such as our database connection string, config required to create a SQLAlchemy engine, and ou SQLAlchemy `Base` declarative mapping class). 
- `[ versions ] ` -> A directory containing each migration to be run. Every file within this directory represents a DB migration, and contains a reference to previous/next migrations so they are always run in the correct sequence.
- `[ script.py.mako ]` -> boilerplate generated by alembic.
- `[ README ]` -> boilerplate generated by alembic.
- `[ alembic.ini ]` -> Tells alembic where to look for the other files, as well as setting up config for logging.

In order to trigger the alembic migrations, you run the `alembic upgrade head command`. When you make any change to a database table, you capture that change by running `alembic revision --autogenerate -m "Some description" ` - this will generate a new file in the `versions` directory which you should always check.

For our recipe API, we've wrapped this migration command in the `prestart.sh` bash script:

~~~
#! /usr/bin/env bash

#Let the DB start
python ./app/backend_pre_start.py

# Run migrations
alembic upgrade head <----- ALEMBIC MIGRATION COMMAND

# Create initial data in DB
python ./app/initial_data.py
~~~
<br>

Running the alembic migrations will not only apply changes to the database, but also create the tables and columns in the first place. This is why you don't find any table creation command like `Base.metadata.create_all(bind=engine)` which you'll often find in tutorials that don't cover migrations.

You'll also notice that we also have a couple of other scripts in our `prestart.sh` script:
- `[ backend_pre_start.py ]` -> which simply executes a SQL `SELECT 1` query to check our DB is working.
- `[ initial_data.py ]` -> which uses the `init_db` function from `db/init_db.py` which we will breakdown further now

<br>

`db/init_db.py`
~~~
from app import crud, schemas
from app.db import base # noqa: F401
from app.recipe_data import RECIPES

logger = logging.getLogger(__name__)
FIRST_SUPERUSER = "admin@recipeapi.com"

def init_db(db: Session) -> None: #[1]
    if FIRST_SUPERUSER:
        user = crud.user.get_by_email(
            db,
            email=FIRST_SUPERUSER
        ) #[2]
        if not user:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=FIRST_SUPERUSER,
                is_superuser=True,
            )
            user = crud.user.create(
                db,
                obj_in=user_in
            )
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
        if not user.recipes:
            for recipe in RECIPES:
                recipe_in = schemas.RecipeCreate(
                    label=recipe["label"],
                    source=recipe["source"],
                    url=recipe["url"],
                    submitter_id=user.id,
                )
                crud.recipe.create(
                    db,
                    obj_in=recipe_in #[3]
                )
~~~
<br>

1. The `init_db` function takes as its only argument a SQLAlchemy `Session` object, which we can import from our `db/session.py`.
2. Then we make use of the `crud` utility functions that we created earlier in this part of the tutorial to fetch or create a user. We need a user so that we can assign a `submitter` to the initial recipes (recall the foreign key lookup from the recipe table to the user table).
3. We iterate over the recipes hardcoded in the `app/recipe_data.py RECIPE` list of dictionaries, use that data to create a series of Pydantic `RecipeCreate` schemas, which we can then pass to the `crud.recipe.create` function to `INSERT` rows into the database.

<br>

Give this a try in your cloned copy:
~~~
cd into the part-7 directory
pip install poetry
run poetry install to install the dependencies
run poetry run ./prestart.sh
~~~

In the terminal, you should see migrations being applied. You should also see a new file created: part-7-database/example.db. This is the SQLite DB, check it by running:

- Install sqlite3
- run the command sqlite3 example.db
- run the command .tables
  
You should see 3 tables: alembic_version, recipe, and user. Check the initial recipe data has been created with a simple SQL query: SELECT * FROM recipe;

You should see 3 recipe rows in the sqlite DB:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-7/sqlite-commands.png)

You can exit the SQLite3 shell with the command `.exit`

Great! All that remains now is to bring everything together in our API endpoints.

<br>

### Pratical Section 4 - Putting it all Together in Our API Endpoints

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-7/diagram-path-operations.jpeg)

<br>

If you look at app/main.py you'll find all the endpoints functions have been updated to take an additional `db` argument:

~~~
from fastapi import Request, Depends
#skipping..

@api_router.get("/", status_code=200)
def root(
    request: Request,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Root GET
    """
    recipes = crud.recipe.get_multi(db = db, limit = 10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "recipes": recipes
        },
    )
    #skipping..
~~~
<br>

This is a first look at FasAPI's powerful `dependency injection capabilities`, which for my money is one of the frameworks best features. Dependency Injection (DI) is a way for your functions and classes to declare things they need to work (in a FastAPI context, usually our endpoint functions which are called `path operation functions`).

We'll be exploring dependecy injection in much more detail later in the turorial. For now, what you need to appreciate is that the FastAPI `Depends` class is used in our function parameters like so:

~~~
db: Session = Depends(deps.get_db)
~~~

And what we pass into `Depends` is a function specifying the dependency. In this part of the tutorial, we've added these functions in the `deps.py` module:

~~~
from typing import Generator

from app.db.session import SessionLocal #[1]

def get_db() -> Generator:
    db = SessionLocal() #[2]
    try:
        yield db #[3]
    finally:
        db.close() #[4]
~~~

<br>

Quick breakdown:

1. We import the ORM session class `SessionLocal` from `app/db/session.py`
2. We instantiate the session
3. we `yield` the session, which returns a generator. Why do this? well, the yield statement suspends the function's execution and sends a value back to the caller, but retains enough state to enable the function to resume where it is left off. In short, it's an efficient way to work with our database connection. `Python generators primer for those unfamiliar`.
4. We make sure we close the DB connection by using the `finally` clause of the `try` block - meaning that the DB session is always `closed`. This releases connection objects associated with the session and leaves the session ready to be used again.

<br>

OK, now understand how our DB session is being made available in our various endpoints. Let's look at more complex example:

~~~
@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe) #[1]
def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single recipe by ID
    """
    result = crud.recipe.get(db = db, id = recipe_id) #[2]
    if not result:
        # the exception is raised, not returned - you will get a validation error otherwise
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with ID {recipe_id} not found",
        )
        return result
~~~
<br>

Notice the following changes:

1. The `response_model=Recipe` now refers to our updated Pydantic `Recipe` model, meaning that it will work with our ORM calls.
2. We use the `crud` utility function to get a recipe by id, passing in the `db` session object we specified as a dependency to the endpoint.

<br>

The extra `crud` utilities took a bit more time to understand - but can you see how now we have an elegant separation of concerns - no need for any DB queries in the endpoint code, it's all handled within our CRUD utitility functions.

We see a similar pattern in the other endpoints, swapping ou `crud.recipe.get` for `crud.recipe.get_multi` when we're returning multiple recipes and `crud.recipe.create` when we create new recipes in the POST endpoint.

<br>


## Part 8 - Project Structure, Settings and API Versioning

<br>

By structuring your FastAPI projects well, you’ll set your REST APIs up for easy extensibility and maintenance later.

This is post borrows heavily from the official full-stack FastAPI postgresql cookie-cutter repo. For learning, the cookie cutter repo is a bit complex, so we’re simplifying things at this point in the series. However, by the end of the tutorial we’ll have something similar.

<br>

### Practical Section 1 - FastAPI Project Structure and Config

<br>

Let's take a look at the new additions to the app directory:

~~~
├── app
│  ├── __init__.py
│  ├── api                     ----> NEW
│  │  ├── __init__.py
│  │  ├── api_v1               ----> NEW
│  │  │  ├── __init__.py
│  │  │  ├── api.py            ----> NEW
│  │  │  └── endpoints         ----> NEW
│  │  │     ├── __init__.py
│  │  │     └── recipe.py      ----> NEW
│  │  └── deps.py
│  ├── backend_pre_start.py
│  ├── core                    ----> NEW
│  │  ├── __init__.py
│  │  └── config.py            ----> NEW
│  ├── crud
│  │  ├── __init__.py
│  │  ├── base.py
│  │  ├── crud_recipe.py
│  │  └── crud_user.py
│  ├── db
│  │  ├── __init__.py
│  │  ├── base.py
│  │  ├── base_class.py
│  │  ├── init_db.py
│  │  └── session.py
│  ├── initial_data.py
│  ├── main.py                  ----> UPDATED
│  ├── models
│  │  ├── __init__.py
│  │  ├── recipe.py
│  │  └── user.py
│  ├── schemas
│  │  ├── __init__.py
│  │  ├── recipe.py
│  │  └── user.py
│  └── templates
│     └── index.html
├── poetry.lock
├── prestart.sh
├── pyproject.toml
├── README.md
└── run.sh
~~~

<br>

As you can see, we've added a new `api` directory. Our purpose here is to unclutter the `main.py` file and allow for API versioning, we'll look at that in the second (versioning) part of this blog post.

We've also now added the `core/config.py` module, which is a standard FastAPI structure. We use Pydantic models in here (as we do for the schemas) to define the app condig. This allows us to make use of Pydantics type inference and validators. Let's look at the `core/config.py` code to illustrate:

~~~
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union

class Settings(BaseSettings): #[1]
    API_V1_STR: str = "/api/v1" #[2]
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins 
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True) #[3]
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startwith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///example.db"
    FIRST_SUPERUSER: EmailStr = "admin@recipeapi.com"

    class Config:
        case_sensitive = True #[4]

settings = Settings() #[5]
~~~
<br>

1. The `settings` class inherits from the `Pydantic BaseSettings` class. This model will attempt to determine the values of any fields not passed as keyword arguments by reading from environment variables of the same name. This is why you won't see code like `API_V1_STR: str = os.environ['API_V1_STR']` because it's already doing that under the hood.
2. As with other Pydantic models, we use type hints to validate the config - this can save us from a lot of error as config code is notoriously poorly tested.
3. Using `Pydantic validator decorators` it's possible to validate config fields using functions.
4. Behaviour of pydantic can be controlled via the `Config class on a model`, in this example we specify that our settings are case-sensitive.
5. Finally we instantiate the `Settings` class so that `app.core.config.settings` can be imported throughout the project.

<br>

You'll see that the code for this part of the tutorial has now been updated so that all significant glocal variables are in the config (e.g. `SQLALCHEMY_DATABASE_URI` , `FIRST_SUPERUSER`).

As the project grows, so too will the complexity of the config (we'll see this soon enough in future parts of the tutorial). This is a useful starting point with enough realism to give a feel for what could be here.

<br>

### Pratical Section 2 - API Versioning

<br>

It's best practice to version your APIs. This allows you to manage breaking API changes with your clients in a more disciplined and structured way. The Stripe API is the gold standard for this, if you'd `like some inspiration`.

Let's start by observing the new API versioning introduced in this part of the tutorial:

- Clone the tutorial `project repo`
- `cd` into part-8
- `pip install poetry` (if you dont have it already)
- `poetry install`
- `poetry run ./prestart.sh` (set up a new DB in this directory)
- `poetry run ./run.sh`
- Open http:://localhost:8001

<br>

You should be greeted by our usual server-side rendered HTML:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-8/root-route.png)

<br>

So far no change. Now navigate to the interactive UI docs at `http://localhost:8001/docs`. You'll notice that the recipe endpoints now are prefaced with `/api/v1`:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-8/versioned-api.jpeg)

<br>

Go ahead and have a play with the endpoints (they should all work exactlu the same as the previous part of the tutorial). We now haver versioning. Let's look at the code changes which have led to this improvement:

`app/api_v1/api.py`

~~~
from fastapi import APIRouter

from app.api.api_v1.endpoints import recipe

api_router = APIRouter()
api_router.include_router(recipe.router, prefix="/recipes", tags=["recipes"])
~~~

Notice how the recipe endpoint logic is pulled in from `app/api.api_v1.endpoints.recipe.py` (where we have extracted the recipe endpoint code from `app/main.py`). We then use the `include_router` method, passing in a prefix of `/recipes`. This means that endpoints defined in the `recipes.py` file which specify a route of `/` will be prefixed by `/recipes`.

Then back in `app/main.py` we continue to stack the FastAPI routers:

~~~
# Skipping...

root_router = APIRouter()
app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

@root_router.get("/",status_code=200)
def root(
    request: Request,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Root GET
    """
    recipes = crud.recipe.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "recipes": recipes
        },
    )

app.include_router(api_router, prefix=settings.API_V1_STR) # API VERSIONING.
app.include_router(root_router)

# Skipping...
~~~

<br>

Once again we use the `prefix` argument, this time with the `API_V1_STR` from our config. In short, we stack prefixes of `api/v1` (from `main.py`) the `recipes` (from `api.py`). This creats the versioned routes we see in the documentation UI.

Now whenever we want to add new logic (e.g. a users API), we can simply define a new module in `app/api/api_v1/endpoints`. If we want to create a v2 API, we have a structure that allows for that.

The other point to note from the above code snippet is that because we do `not` apply any versioning prefix to our root route (the home route Jinja tempalte), the this one endpoint is not versioned.


### Links


<br>


## Part 9 - Asynchronous Performance Improvement

<br>

There are two main reasons why FastAPI is called "Fast":

1. Impressive framework performance
2. Improved developer workflow

<br>

In this post, we'll be exploring the performance element(1). If you're comfortable with Python's `asyncio` module, you can skip down to the practical part of the post. If not, let's talk theory for a bit.

<br>

### Theory Section - Python Asyncio and Concurrent Code

<br>

A quick bit of terminology. In programming, concurrency means:

> Executing multiple tasks at the same time but not necessarily simultaneously

<br>

On the other hand, doing things in parallel means:

> Parallelism means that an application splits its task up into smaller subtasks which can be processed in parallel, for instance on multiple CPUs at the exact same time.

<br>

More pithily:

> Concurrency is about dealing with lots of things at once. Parallelism is abut doing lots of things at once.

This `stackoverflow thread` has some great further rading in the answers/comments.

For years, options for writing asynchronous code in Python were suboptimal - relying on the limited `asyncore` and `asynchat` modules (both now deprecated) or third-party libraries like `gevent` or `Twisted`. The in Python 3.4 the `asyncio` library was introduced. This was one of the most significant additions to the Python language in its history, and from the initial `PEP-3156` (well worth a read), there were many subsequent improvements, such as the introduction of `async` and `await` syntax in `PEP-492`. These changes to the language have resulted in a sudden Python ecosystem renaissance, as new tools which make use of `asyncio` were (and continue to be) introduced, and other libraries are updated to make use of the new capabilities. FastAPI and Starlette (which is the foundation of FastAPI) are examples of these new projects.

By leveraging Python's new Asynchronous IO (async IO) paradigm (which exists in many other languages), FastAPI has been able to come up with very impressive benchmarks (on par with nodejs or golang):

![](https://christophergs.com/assets/images/fastapi_flask_post/benchmarks.jpeg)

> Naturally, benchmarks should be taken with a pinch of salt, have a `look at the source of these`

<br>

Async IO is a great fit for IO-bound network code (which is most APIs), where you have to wait for something, for example:

- Fetching data from other APIs
- Receiving data over a network (e.g. from a client browser)
- Querying a database
- Reading the contents of a file

<br>

Async IO is not threading, nor is it multiprocessing. In fact, async IO is a single-threaded, single-process design: it uses cooperative multitasking. For more on the trade-offs of these different approaches see this `great article`.

If you're still confused check out two great analogies:
- `Miguel Grinberg's multiple chess games analogy`
- `Sebastián Ramírez (Tiangolo)'s fast food analogy`

<br>

In any Python program that uses `asyncio`, there will be an `asyncio event loop`

> The event loop is the core of every asyncio application. Event loops run asynchronous tasks and callbacks, perform network IO operations, and run subprocesses.

<br>

With basic examples, you'll see this kind of code:

~~~
async def main():
    await asyncio.sleep(1)
    print('hello')

asuncio.run(main())
~~~

<br>

When you see a function defined with `async def` it is a special function called a `coroutine`. The reason why coroutines are special is that they can be paused internally, allowing the program to execute them in increments via multiple entry points for suspending and resuming execution. This is in contrast to normal functions which only have one entry point for execution.

Where you see the `await` keyword, this is instructing the program that is a "suspendable point" in the coroutine. It's a way for you to tell Python "this bit might take a while, fell free to go and do something else".

In the above code snippet, `asyncio.run` is the highlevel API for executing the coroutine and also managing the asyncio event loop.

With FastAPI (and uvicorn our ASGI server), the management of the event loop is taken care of for you. This means that the main things we need to concern ourselves with are:

- Declaring API path operation endpoint functions (and any downstream functions they depend on) as coroutines via `async def` where appropriate. If you do this wrong, FastAPI is still able to handle it, you just won't get the performance benefits.
- Declaring particular points as awaitable via the `await` keyword within the coroutines.

<br>

### Practical Section - Async IO Path Operations

Let's take a look at the new additions to the app directory in part-9:

~~~
├── app
│  ├── __init__.py
│  ├── api
│  │  ├── __init__.py
│  │  ├── api_v1               
│  │  │  ├── __init__.py
│  │  │  ├── api.py            
│  │  │  └── endpoints         
│  │  │     ├── __init__.py
│  │  │     └── recipe.py      ----> UPDATED
│  │  └── deps.py
│  ├── backend_pre_start.py
│  ├── core                    
│  │  ├── __init__.py
│  │  └── config.py            
│  ├── crud
│  │  ├── __init__.py
│  │  ├── base.py
│  │  ├── crud_recipe.py
│  │  └── crud_user.py
│  ├── db
│  │  ├── __init__.py
│  │  ├── base.py
│  │  ├── base_class.py
│  │  ├── init_db.py
│  │  └── session.py
│  ├── initial_data.py
│  ├── main.py                 ----> UPDATED
│  ├── models
│  │  ├── __init__.py
│  │  ├── recipe.py
│  │  └── user.py
│  ├── schemas
│  │  ├── __init__.py
│  │  ├── recipe.py
│  │  └── user.py
│  └── templates
│     └── index.html
├── poetry.lock
├── prestart.sh
├── pyproject.toml
├── README.md
└── run.sh
~~~

To follow along:

- Clone the tutorial `project repo`
- `cd` into part-9
- `pip install poetry`  (if you don't have it already)
- `poetry install`
- `poetry run ./prestart.sh` (sets up a new DB in this directory)
- `poetry run ./run.sh`
- Open http://localhost:8001

<br>

You should be greeted by our usual server-side rendered HTML:
![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-8/root-route.png)

<br>

So far no change. Now navigate to the interactive swagger UI docs at `http://localhost:8001/docs`. You'll notice that the recipe REST API endpoints now include:
- `/api/v1/recipes/ideas/async`
- `/api/v1/recipes/ideas`

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-9/new-recipe-endpoints.jpeg)

<br>














