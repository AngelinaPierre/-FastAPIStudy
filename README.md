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














