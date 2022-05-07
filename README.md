poetry run python ./prestart.py

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

These are two new endpoints that both do the same thing: fetch top recipes from three different subreddits and return them to the client. Obviously, this is for learning purposes, but you can imagine a scenario where our imaginary recipe API business wanted to offer API users a "recipe idea" feature.

Let's have a look at the code for the non-async new endpoint: `app/api_v1/endpoints/recipe` py file.

~~~
import httpx #[1]

#Skipping...

def get_reddit_top(sbreddit: str, data: dict) -> None:
    response = httpx.get(
        f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
        headers = {"User-agent": "recipe bot 0.1"},
    ) #[2]
    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data

@router.get("/ideias/")
def fetch_ideas() -> dict:
    data: dict = {} #[3]
    get_reddit_top("recipes", data)
    get_reddit_top("easyrecipes", data)
    get_reddit_top("TopSecretRecipes", data)


    return data

# Skipping...

~~~

<br>

Let's break this down:

1. We're introducing a new library called `httpx`. This is an HTTP client similar to the `request library` which you might be more familiar with. However, unlike `requests`, `httpx`, can handle async calls, so we use it here.
2. We make a `GET` HTTP call ro reddit, grabbing the first 5 results.
3. The `data` dictionary is updated in each call to `get_reddit_top`, and then returned at the end of the path operation.

<br>

Once you get your head around the reddit API call, this sort of code should be familiar (if it's not, backtrack a few sections in the tutorial series).

Now let's look at the async equivalent endpoint:

`app/api_v1/endpoints/recipe.py`

~~~
import httpx
import asyncio #[1]
#Skipping...

async def get_reddit_top_async(subreddit: str, data: dict) -> None: #[2]
    async with httpx.AsyncClient() as client: #[3]
        response = await client.get( #[4]
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "recipe bot 0.1"},
        )
    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data

@router.get("/ideias/async")
async def fetch_ideas_async() -> dict:
    data: dict = {}

    await asyncio.gather(#[5]
        get_reddit_top_async("recipes", data),
        get_reddit_top_async("easyrecipes", data),
        get_reddit_top_async("TopSecretRecipes", data),       
    )

    return data

#Skipping...
~~~
<br>

OK, let's break this down:

1. Although it isn't always necessary, in this case we do need to import `asyncio`
2. Notice the `get_reddit_top_async` function is declared with the `async` keyword, defining it as a cotoutine.
3. `async with httpx.AsyncClient()` is the `httpx` context manager for making async HTTP calls.
4. Each GET request is made with the `await` keyword, telling the Python that this is a point where it can suspend execution to go and do something else.
5. We use the `asyncio.gather` to run a sequence of awaitable objects(i.e. our coroutines) concurrently.

<br>

Point 5 isn't shown explicitly in the FastAPI docs, since it's to do with usage of `asyncio` rather than FastAPI. But it's easy to miss that you need this kind of extra code to really leverage concurrency.

In order to test our new endpoints, we'll add a small bit of middleware to track response times. `Middlewares` is a function that works on every request before it is processed by any specific `path operatation`. We'll look at more Middleware later in the tutorial series. For now you just need to know that it will time our new endpoints.

In `app/main.py`

~~~
# Skipping...

@app.middleware("http")
async def add_process_time_header(resquest: Request, call_next):
    start_time = time.time()
    respose = await call_next(resquest)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] - str(process_time)
    return response

#Skipping...
~~~

<br>

Great! Now let's open up our interactive API documentation at `http://localhost:8001/docs` and try out the new endpoints:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-9/docs-try-it.jpeg)

<br>

When you click the `execute` button, you'll see a new addition in the response headers:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-9/docs-response-headers.jpeg)

<br>

Notice the `x-process-time` header (highlighted in the screegrab above). This is how we can easily compare the times of the two endpoints. If you try both `/api/v1/recipes/ideas/async` and `/api/v1/recipes/ideas`, you should see that the `async` end point is 2-3x faster.

We’ve just tapped into FastAPI’s high-performance capabilities!

<br>

### Notes on Async IO and Third Party Dependencies like SQLALchemy
<br>

After the euphoria of the previous section, you might be temoted to think you can just plonk `async` and `awaits` for any and every IO call to get a performance speed up. One obvious place to asume this is with database queries (another classic IO operation).

Not so fast i'm afraid.

Every library that you attempt to `await` needs to support async IO. Many do not. SQLAlchemy only introduced this compatibility in `version 1.4` and there are a lot of new things to factor in like:

- DB drivers which support async queries
- New query syntax
- Creating the engine & session with new async methods

We'll be looking at this later in the tutorial series in the advanced part.


<br>

## Part 10 - Auth via JSON Web Token (JWT)

<br>

### Theory Section - JWT Auth Overview

<br>

#### What do We Mean by Auth: Authentication vs. Authorization

<br>

When people talk about "auth" they are talking about:

1. Authentication: Determines whether users are who they claim to be
2. Authorization: Determines what users can and cannot acces

<br>

In short, access to a resource is protected by both authentication and authorization. If you can't prove your identity, you won't be allowed into a resource. And even if you can prove your identity, if you are not authorized for that resource, you will still be denied access.

Most of what we're covering in this tutorial is authentication, but it lays the foundation necessary for authorization.

#### What's a JWT?

<br>

JSON Web Token (JWT, stupidly pronounced "jot") is an open standard (`RFC 7519`) that defines a way for transmitting information - like authentication and authorization facts - between two parties: an issuer and an audience. Communication is safe because each token issued is digitally signed, so the consumer can verify if the token is authentic or has been forged. There are quite a few different ways to sign the token which are `discussed in more detail in here` (link)

A JSON Web Token is basically a long encoded text string. This string is consists of threee smaller parts, separated by a period. These parts are:

- The header
- A payload or body
- A signature

<br>

Therefore, tokens will look like this: `header.payload.signature`

JSON web tokens are not "secrets" (unless you choose to encrypt them) like API tokens. However, because they are signed they cannot be easily tampered with - this is their value. JWTs are designed to be passed around. In fact, here is one for our example app which you can copy and paste into `jwt.io` to play with:

~~~
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjI5NzMyNzY2LCJpYXQiOjE2MjkwNDE1NjYsInN1YiI6IjUifQ.rJCd2LxtEn5hJz3OASul0bhHf2GlFKfCNNk48q0pb4o
~~~

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/jwt-io.jpeg)

<br>

Notice the decoded section on the right consist of three parts.


#### Why Use JWTs?

<br>

It all comes down to state. The HTTP protocal is stateless, so when calling protected API endpoints our options are:

1. Send a username/password for `every request`
2. Something smarter than (1)

<br>

With JWTs, the client (e.g. a user's browser) will store a copy of the JWT after logging in and then include it in subsequent request headers. On the server, this token is decoded and verified. This means there is no need for every protected endpoint request to include login credentials.

Typical JWT auth use cases include:

- A non-server-side rendered web frontend, such as one written in a frontend framework like React, Angular or Vue.
- A backend microservice
- An external service
- A mobile app
- A desktop app

<br>

This tutorial serie's project, a recipe API, is a realistic scenario where we would want an auth solution.

There are alternatives to JWTs such as:
- Fernet
- Branca
- Platform-Agnostic Security Tokens(PASETO)

<br>

The pros and cons of these `alternatives are discussed here` (link). I am not a security expert, so do your research. This post assumes that you have decided to go down the JWT route (which is very popular). Let's get coding!

<br>

### Pratical Section 1 - Implementing JWT Auth Endpoints - Sign Up Flow

<br>

Let's take a look at the new additions to the app directory in part 10:

~~~
./app
├── __init__.py
├── api
│  ├── __init__.py
│  ├── api_v1
│  │  ├── __init__.py
│  │  ├── api.py          ----> UPDATED
│  │  └── endpoints
│  │     ├── __init__.py
│  │     ├── auth.py      ----> ADDED
│  │     └── recipe.py
│  └── deps.py            ----> UPDATED
├── backend_pre_start.py  ----> UPDATED
├── core
│  ├── __init__.py
│  ├── auth.py            ----> ADDED
│  ├── config.py          ----> UPDATED
│  └── security.py        ----> ADDED
├── crud
│  ├── __init__.py
│  ├── base.py
│  ├── crud_recipe.py
│  └── crud_user.py       ----> UPDATED
├── db
│  ├── __init__.py
│  ├── base.py
│  ├── base_class.py
│  ├── init_db.py
│  └── session.py
├── initial_data.py
├── main.py
├── models
│  ├── __init__.py
│  ├── recipe.py
│  └── user.py            ----> UPDATED
├── schemas
│  ├── __init__.py
│  ├── recipe.py
│  └── user.py            ----> UPDATED
└── templates
   └── index.html
~~~

<br>

To follow along:

- Clone the tutorial `project repo`
- cd into part-10
- pip install poetry (if you don’t have it already)
- poetry install
- If you’re continuing from part 9, remove your SQLite database rm example.db as we’ve made some breaking changes to the DB schema (ignore if you’re starting here)
- poetry run ./prestart.sh (sets up a new DB in this directory)
- poetry run ./run.sh
- Open http://localhost:8001

<br>

To begin, we've added three new endpoints to our recipe API. These are in the `app/api_v1/endpoints/auth.py` module. We'll start by considering the new `/sigup` POST endpoint where we will create new users:

~~~
@router.post("/sigup", response_module=schemas.User, status_code=201) #[1]
def create_user_sigup(
    *,
    db: Session = Depends(deps.get_db) #[2]
    user_in: schemas.user.UserCreate, #[3]
) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = db.query(User).filter(User.email == user_in.email).first() #[4]
    if user:
        raise HTTPException( #[5]
            status_code = 400,
            detail = "The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in) #[6]

    return user
~~~
<br>

1. As show in `Part 4 of the series` we specify a Pydantic `response_model` which shapes the endpoint JSON response.
2. As show in `Part 7 of the series` we specify the database as a dependecy of the endpoint via FastAPI's dependecy injection capabilities.
3. The POST request body is validated according to the `UserCreate` pydantic schema. There are some really powerfull tweaks we've made in the user schemas we will cover shortly.
4. As covered in `Part 7 of the series` we use the SQLAclhemy ORM to query the database `user` table, applying a filter to check if any users with the requested email already exist.
5. In order to ensure user emails are unique, if a matching user is found (i.e. an existing user with the same email address) then we return an HTTP 400 (as show in `Part 5: Basic Error Handling`)
6. Finally, if the user email is unique we proceed to use the `crud` utility functions to create the user. We'll take a look at this now.

<br>

If we follow the code logic, we arrive at the call to `crud.user.create(db=db, obj_in=user_in)`. let's take a look at this code in `app/crud/crud_user.py`:

~~~
from typing import ANy, Dict, Optiona, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class CRUDUser(CRUDBase[User, Usercreate, UserUpdate]):
    def get_by_email(
        self,
        db: Session,
        *,
        email: str
    ) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(
        self,
        db: Session,
        *,
        obj_in: UserCreate
    ) -> User:
        create_data = obj_in.dict()
        create_data.pop("password")
        db_ojb = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()

        return db_obj
    # Skipping...
user = CRUDUser(User)
~~~

<br>

We need to consider this code alongside the updated `UserCreate` schema in `app/schemas/user.py` which now includes the `password` field:

~~~
# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
~~~
<br>

Crucially, you'll note that in the `create` method (note that we're `overriding` the parent `CRUDBase` method), we convert the Pydantic model to a dictionary by calling `obj_in.dict()` and the remove the `password` entry from the dictionary via `.pop()`. Then to generate the hashed password we call a new method `get_password_hash`. Let's look at this function next.

When a password has been "hashed" it means it has been turned into a scrambled representation of itself. A user's password is taken and - using a key known to the site - the hash value is derived from the combination of both the password and the key, using a set algorithm. IN the recipe API, we'll use the `passlib` library to help us with this functionality. From the docs:


> Passlib is a password hashing library for Python 2 & 3, which provides cross-platform implementations of over 30 password hashing algorithms, as well as a framework for managin existing password hashes. It's designed to be useful for a wide range of tasks, from verifying a hash found in /etc/shadow, to providing full-strength password hashing for multi-user application.

<br>

This library can be seen in use in the `app/core/security.py` module:

~~~
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password:str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)

#Skipping...
~~~

<br>

Here the `CryptContext` class from `passlib` is used to hash and verify user passwords.

The last step in the user creation flow is updating our database. We'll have to make one change to the `user` table:

~~~
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    recipes = relationship(
        "Recipe",
        cascade="all, delete-orphan",
        back_populates="submitter",
        uselist=True,
    )

    # New Addition
    hashed_password = Column(String, nullable=False)
~~~

<br>

Notice the new column `hashed_password`.

So this is our flow to create a user. Those following along from previous tutorial posts will note that i've tweaked the alembic migration and the `app/db/init_db.py` script to accomodate creating users with a password.

<br>

### Pratical Section 2 - Implementing JWT Auth Endpoints - Login Flow

<br>

Next, let's consider the new `/login` endpoint:

~~~
from fastapi.security import OAuth2PasswordRequestForm
#Skipping...

@router.post("/login")
def login(
    db: Session = Depends(deps.get_db), forma_data: OAuth2PasswordRequestForm = Depends() #[1]
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request
    """

    user = authenticate(email=form_data.username, password=form_data.password, db = db) #[2]
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password) #[3]
    
    return {
        "access_token": create_access_token(sub=user.id), #[4]
        "token_type": "bearer",
    }
# Skipping...
~~~

<br>

Notice that we use FastAPI's `OAuth2PasswordRequestForm dependency` in the path operation function.

`OAuth2PasswordRequestForm` is a class dependency that declares a form body with:
- The username.
- The password.
- An optional grant_type
- An optional scope field as a big string, composed of strings separated by spaces. (not required for our example)
- An optional client_id (not required for our example).
- An optional client_secret (not required for our example).

<br>

Let's break the endpoint logic down:

1. We declare the `OAuth2PasswordRequestForm` dependency
2. We check the request body via a new `authenticate` function (we'll look at this in a moment)
3. If authentication fails, no user is returned, this triggers an HTTP 400 response.
4. Finally, the JSON web token is created and returned to the client via the `create_access_token` function (we'll look at this in a moment).

<br>

Both of the new functions in the above list (`authenticate` and `create_access_token`) are from the new `app/core/auth.py`
module. Let's consider this module in its entirety now. You'ill note that at this point in the tutorial series we've introduced another external dependency, `pyhon-jose` which provides us with a variety of cryptographic backends for encrypting and signing tokens.

~~~
from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from app.models.user import User
from app.core.config import settings
from app.core.security import verify_password

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = db.query(User).filter(user.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password): #[1]
        return None
    return user


def create_access_token(*,sub: str) -> str: #[2]
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), #[3]
        sub=sub,
    )

def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire #[4]
    payload["iat"] = datetime.utcnow() #[5]
    payload["sub"] = str(sub) #[6]

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM) #[7]
~~~

<br>

Quite a lot is happening here, let's break it down:

1. We use the verify_password function we looked at earlier in `app/core/security.py` which leverages the passlib library.
2. The `sub` keyword argument to the `create_access_token` function will correspond to the user ID.
3. The `app/core/config.py` is updated to include some auth-related settings, such the JWT validity timeframe before expiry
4. We construct the JWT. There are a number of required/optional fields( known as "claims") detailed in `RFC 7519`. The "exp" (expiration time) claim identifies the expiration time on or after which the JWT MUST NOT be accepted for processing.
5. The "iat" (issued at) claim identifies the time at which the JWT was issued.
6. The "sub" (subject) claim identifies the principal that is the subject of the JWT. THis will be the user ID in our case.

<br>

If the user passes the authentication check, the `/login` endpoint return the JWT to the client. This JWT can then be used to access restricted functionality. A basic example of this is found in the third new endpoint:

~~~
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user
~~~

<br>

Up until now, the only dependency injection we've used has been for accessing the database, but we can also use it for other things, like fetching the logged-in user. We'll explore this in more detail in the next post of the series on dependency injection.

The key code to note from the updated `app/deps.py` module is here:

~~~
def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    # Skipping for simplicity...
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"Verify_aud": False},
        )
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
    # Skipping for simplicity...
~~~

<br>

Here the incoming JWT token is decoded ( again using python-jose), with the combination of a `JWT-SECRET` value set in the API `app/core/config.py` as well as the encoding algorithm configured there (HS256). If this decoding is successful we "trust" the token, and are happy to fetch the user from the database.

For now, let's try out the whole auth flow locally:

- Clone the tutorial project repo
- cd into part-10
- pip install poetry (if you don’t have it already)
- poetry install
- If you’re continuing from part 9, remove your SQLite database rm example.db as we’ve made some breaking changes to the DB schema (ignore if you’re starting here)
- poetry run ./prestart.sh (sets up a new DB in this directory)
- poetry run ./run.sh
- Open http://localhost:8001/docs

<br>

You should see the new endpoints:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/new-auth-endpoints.jpeg)


<br>

Let's curl `api/v1/auth/me` endpoint via the `Try Me` button:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/auth-me-endpoint.jpeg)

<br>

When you hit this endpoint, you should see the response is a 401 Unauthorized:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/not-authenticated.jpeg)

<br>

To fix this, we will first create a user via the `api/v1/auth/signup` endpoint. Once again use the `Try Me` functionality and populate the request body fields (first)name, surname, email, password) then click "execute";

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/create-user.jpeg)

<br>

If you scroll down, you should see in the response that your user has been created:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/create-response.jpeg)

<br>

Next, we'll make use of a useful swagger interactive UI feature to Authorize a user. Click on the `Authorize` button in the top right:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/authorize-button.jpeg)

Enter the credentials (note you should enter the `email address in the username field`) than click "Authorize":

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/filled-authorize.jpeg)

<br>

You should see that you are logged in. Now if you try the `api/v1/auth/me` endpoint again, you should get a 200 response with the user details in the response body:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-10/successful-call.jpeg)

<br>

Congrats! You now have basic auth working in your FastAPI application!

There are more complicated features we could add like:
- Using scopes for authorization
- Refresh tokens
- Password resets
- Single Sign On (SSO)
- Adding custom data to the JWT payload
- JSON Web Encryption

<br>

We'll be looking at all of this in the tutorial series in the advanced part.

<br>

## Part 11 - Dependency Injection via FastAPI Depends

<br>

### Theory Section - What is Dependency Injection

<br>

Dependency injection (DI) is a way for your code functions and/or classes to declare things they need to work.

If you want to get more technical: Dependency injection relies on composition, and is a method for achieving `inversion of control`.

FasAPI has an elegant and simple `dependency injection system`. It is my favorite feature of the framework. You can declare dependencies in your `path operation functions`, i.e. the decorated functions which define your API endpoints. Typical examples of the sorts of dependencies you might want to inject:
- Database connections
- Auth/security requirements (e.g. getting user credentials, checking the user is active, checking user access level)
- Clients for interacting with other services (e.g. AWS services, email marketing services, a CMS)
- Virtually any shared code logic.

<br>

These dependencies only need to be declared once and then referenced elsewhere in the codebase, so DI makes your code less repetitive and easier to understand. DI is also extremely useful for testing, because you can inject test `doubles` into your objects which reduces unwieldy `monkey patching`. We'll look at an example of this in the second part of the post. Let's start Looking at some examples.

<br>

### Practical Section 1 - Using Di in FastAPI

<br>

To begin, i'll flag which files have changed in the accompanying example code repo `app` directory in this part compared to the previous part:

~~~
./app
├── __init__.py
├── api
│  ├── __init__.py
│  ├── api_v1
│  │  ├── __init__.py
│  │  ├── api.py
│  │  └── endpoints
│  │     ├── __init__.py
│  │     ├── auth.py      
│  │     └── recipe.py    ----> UPDATED
│  └── deps.py            ----> UPDATED
├── clients               ----> ADDED
│  ├── __init__.py          
│  └── reddit.py          ----> ADDED
├── core
│  ├── __init__.py
│  ├── auth.py            
│  ├── config.py          
│  └── security.py
├── crud
│  ├── __init__.py
│  ├── base.py
│  ├── crud_recipe.py
│  └── crud_user.py
├── db
│  ├── __init__.py
│  ├── base.py
│  ├── base_class.py
│  ├── init_db.py
│  └── session.py
├── models
│  ├── __init__.py
│  ├── recipe.py
│  └── user.py            ----> UPDATED
├── schemas
│  ├── __init__.py
│  ├── recipe.py
│  └── user.py            ----> UPDATED
├── templates
|   └── index.html
└── tests                   ----> ADDED
│  ├── conftest.py          ----> ADDED
│  └── api                  ----> ADDED
│      ├── __init__.py
│      └──  test_recipe.py  ----> ADDED
├── backend_pre_start.py
├── initial_data.py
└── main.py
~~~

<br>

So far in the tutorial series, we've already started using FastAPI's dependency injection system for our database session and auth. Let's revisit these and the look at a new example.

#### Injecting The Database Session Dependency

<br>

In `app/api/deps.py` we have a central location where our dependencies are defined. In previous sections we've defined this function to inject our database session into the path operation functions:

~~~
def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()
~~~
<br>

Then we make use of the DB session like so (example taken from `app/api/api_v1/endpoints/recipe.py`):

~~~
from fastapi import Depends
#other imports skipped for brevity

@router.get("/{recipe_id}", status_code = 200, response_model=Recipe)
def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db), #[1] The dependency injection
) -> Any:
    """
    Fetch a single recipe by ID
    """
    result = crud.recipe.get(db=db, id=recipe_id) #[2] Using the dependency
    # code continues...
~~~

<br>

You can see at note [1] in this code snippet the structure for a dependency injection in FastAPI:
- Define a `callable` (usually a function, but it can also be a `class in rarer cases`) which returns or yields*** the instantiated object (or simple value) you wish to inject
- Add a parameter to your path operation function (i.e. the decorated API endpoint function), using the FastAPI `Depends` class to define the parameter, and passing your function to the `Depends` class.

***Note that the typical use-case for a dependency function uses `yield` is where you are doing extra steps after finishing (such as closing a DB connection, clean up, some state mutation).

The dependency is the available for use, as show at note [2] in the code snippet above, where the database session is passed to the crud utility method (which in turn performs a database query via the session, see the `source code`).

There is no "registration" (or similar) process for your functions, FastAPI takes care of that for you under the hood. As `per the docs` it is up to you whether you want your dependency functions to be async or not.

<br>
#### A new Dependency Injection Example - Reddit Client

<br>

In part 11, the example code has changed with the addition of a reddit client dependency. The `get_reddit_top` function used in the `recipe/ideas` endpoint has been replaced. Instead, we've now defined a reddit client in `app/clients/reddit.py`:

~~~
# reddit.py

from httpx import Client, Response

class RedditClient:
    base_url: str = "https://www.reddit.com"
    base_error = t.Type[RedditClientError] = RedditClientError

    def __init__(self) -> None:
        self.session = Client() #[1]
        self.session.headers.update(
            {
                "Content-type": "application/json",
                "User-agent": "recipe bot 0.1",
            }
        )
    
    def _perform_request(
        self, method: str, path: str, *args, **kwargs
    ) -> Response:
        res = None
        try:
            res = getattr(self.session, method)(
                f"{self.base_url}{path}", *args, **kwargs
            ) #[2]
            res.raise_for_status() #[3]
        except HTTPError:
            raise self.base_error(
                f"{self.__class__.__name__} request failure:\n"
                f"{method.upper()}: {path}\n"
                f"Message: {res is not None and res.text}",
                raw_response = res,
            )
        return res
    
    def get_reddit_top(
        self, *, subreddit: str, limit=5
    ) -> dict:
        """Fetch the top n entries from a given subreddit"""

        # If you get empty responses from the subreddit calls, set t=month instead.
        url = f"/r/{subreddit}/top.json?sort=top&t=week&limit={limit}"
        response = self._perform_request("get", url) #[4]
        subreddit_recipes = response.json()
        subreddit_data = []
        for entry in subreddit_recipes["data"]["children"]:
            score = entry["data"]["score"]
            title = entry["data"]["title"]
            link = entry["data"]["url"]
            subreddit_data.append(f"{str(score)}: {title} ({link})")

        return subreddit_data #[5]
~~~

<br>

Let's break this down, as there are a couple of subtleties to this code. Feel free to skip as the key thing to understand is that it's a basic reddit HTTP client:

1. Whilst most Pythonistas are familiar with the popular `requests HTTP client` fewer are familiar with an alternative called `httpx`, which has a similar clean interface but also elegantly supports async. When we use the httpx `Client` this is analagous to requests `Session`, i.e. for `reusing connections via pooling`.
2. Little bit of an ugly method which uses `getattr` to fish out the appropriate method (`get`,`post` etc.) on the session, then immediately invokes it with the correct URL.
3. Like requests, `raise_for_status` raises an error on any 4xx or 5xx responses (`docs`)
4. Usage of the method described in point 2.
5. The data is now returned instead of just mutating the dictionary as in the previous (sub-optimal) function.

<br>

Great, now that we have our client, we need to update the `deps.py` module to include it:

~~~
# deps.py

from app.clients.reddit import RedditClient

def get_reddit_client() -> RedditClient:
    return RedditClient()
~~~
<br>

Nice and simple, we return an instance of the reddit client. The last step is to inject the dependency in our path operation function:

~~~
# api/api_v1/endpoints/recipe.py

from app.api import deps

# code omitted for brevity...

@router.get("/ideas/")
def fetch_ideas(
    reddit_client: RedditClient = Depends(deps.get_reddit_client)
) -> dict:
    data: dict = {}
    for subreddit in ["recipes", "easyrecipes", "TopSecretRecipes"]:
        entry = reddit_client.get_reddit_top(subreddit=subreddit)
        data[subreddit] = entry

    return data
~~~

<br>

Now the reddit client is available within the path operation function. Elegant, isn't? For an ideia of what it would take to build this yourself, you can check out `my post on Flask-Injector`.

The next things to do is to run the `example repo` locally. Follow the setup series in the readme to install the dependencies and start the app. Then head over to `http://localhost:8001/docs` for the interactive UI. Find the `/api/v1/recipes/ideias endpoint and click` Try it out, `then` execute.

You should see a response of this format:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-11/swagger.png)

<br>

Play with the reddit client code (e.g. the parameters in the request in `reddit.py`) to get a feel for how everything hangs together. Experimentation will teach far better than readding.

There is another major benefit to the dependency injection refactoring of the `/recipes/ideas` endpoint, which is in testing. We'll look at that in the second-half of this post. First, let's look at a more complex sub-dependency example.

<br>

#### Using FastAPI Depends Sub-Dependencies - Auth Example

<br>

Your dependencies can also have dependencies. FastApi takes care of solving the hierarchy of dependencies. This adds significant assitional power to the FastAPI DI System. in the `part 10` of the tutorial we saw the `get_current_user` auth dependency:

~~~
# deps.py (part 10)
from fastapi import Depends, HTTPexception, status
from app.core.auth import oauth2_scheme
#omitted

async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        # omitted for brevity....
~~~

<br>

This makes use of the `FastAPI's OAuth2PasswordBearer` wrapping it, so it can be injected in API endpoints.

But what if we want to increase the specificity of our authorization? Let's look at using a sub-dependency to create a callable which restricts the returned users to superusers:

~~~
# deps.py (part11)
# ommited for brevity...

def get_current_active_superuser(
    current_user: User = Depends(get_current_user), #[1]
) -> User:
    if not crud.user.is_superuser(current_user): #[2]
        raise HTTPException(
            status_code = 400,
            detail= "The user doesn't have enough privileges",
        )
    return current_user
~~~
<br>

Two things to breakdown:

1. We pass a dependency to this function (thereby creating a sub-dependency). In this case it is the original `get_current_user` function. This will make the `current` user instance available for use in the function.
2. Then we perform an additional check (using the data access utility `CRUDUser` class methods) for whether the user is a superuser.

<br>

Let's see this in the endpoint code:

~~~
# api/api_v1/endpoints/recipe.py
# omitted...

@router.get("/ideas/async")
async def fetch_ideas_async(
    user: User = Depends(deps.get_current_active_superuser), #[1]
) -> dict:
    data: dict = {}

    await asyncio.gather(
        get_reddit_top_async("recipes", data),
        get_reddit_top_async("easyrecipes", data),
        get_reddit_top_async("TopSecretRecipes", data),
    )

    return data
~~~
<br>

We've now updated this endpoint so that any attempt to call it from a user that is not a superuser will be rejected.

You can test this out by running the example repo, then creating a new user (making them a superuser) via the `/api/v1/auth/signup` endpoint (being sure to update the `superuser` field to `true`)

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-11/superuser.png)

<br>

Once you've created the superuser, you can login via the `Authorize` button in the top right of the OpenAPI interactive UI:

![FastAPI dependency tree example](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-11/authize.png)


<br>

Without being a logged in superuser, attempts to use the `/ideas/async` endpoint will fail (note, the synchronous endpoint wil still work wothout auth as we have not added the dependency to that path operation function).

You could use this sub-dependency approach to build out complex auth logic, as shown in this diagram:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-11/tree.png)


<br>

And naturally, sub-dependencies are not just limited to auth, you can use them in numerous ways.

<br>

### Practical Section 2 - Dependency Injection Implications for Testing

<br>

In this part we added the first test to our example app. The test runner is pytest.

If you're not familiar with pytest, checkout this `free pytest introduction lecture`(link) from my testing and monitoring ML models course.

For the purposes of this tutorial, the key thing to understand is that test fixtures in pytest are defined by convention in a file called `conftest.py`. So in our loan test file `app/tests/api/test_recipe.py` we have a relatively short bit of code hiding a lot more:

~~~
# test_recipe.py
fom app.core.config import settings

def test_fetch_ideas_reddit_sync(client): #[1]
    # When
    response = client.get(f"{settings.API_V1_STR}/recipes/ideas/")
    data = response.json()

    # Then
    assert response.status_code == 200
    for key in data.key():
        assert key in ["recipes", "easyrecipes", "TopSecretRecipes"]
~~~
<br>

The key thing to note at comment [1] where the test takes the `client` as its first argument. `client` is a test fixture defined in `conftest.py`:

~~~
# conftest.py
from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api import deps

async def override_reddit_dependency() -> MagicMock:
    mock = MagicMock() #[4]
    reddit_stub = {
        "recipes": [
            "baz",
        ],
        "easyrecipes"? [
            "bar",
        ],
        "TopSecretRecipes": [
            "foo"
        ],
    }
    mock.get_reddit_top.return_value = reddit_stub #[5]
    return mock


@pytest.fixture() #[1]
def client() -> Generator:
    with TestClient(app) as client: #[2]
        app.dependency_overrides[deps.get_redit_client] = override_reddit_dependency #[3]
        yield client #[6]
        app.dependency_overrides = {} #[7]
~~~
<br>

There is a lot happening here, let's break it down by the comment numbers:

1. We use the `pytest fixture decorator` to define a fixture
2. We access the FastAPI built-in `test client` via a context manager so we can easily perform clean-up (see 7)
3. We use the `FastAPI app dependency_overrides` to replace dependencies. We replace what the selected dependency (in this case `get_reddit_client`) callable is, pointing to a new callable which will be used in testing (in this case `override_reddit_dependency`)
4. We make use of the Python standard library unittest mock `MagicMock (docs for those unfamiliar)`(link)
5. We specify the return value of a particular method in our mocked reddit client (`get_reddit_top`), here it will return dummy data
6. We `yield` the modified client
7. We perform clean up on the client, reverting the dependencies.

<br>

This is an illustration of the power of dependency injection in a testing context. Whilst libraries like `request-mock` would also allow you to replace the return value of a particular HTTP call, we can also apply this approach to any callable, whether it's:
- Interacting with a database
- Sending emails via SMTP
- Working with other protocols (e.g. ProtoBuf)
- Simply calling complex code we don't need to worry about for a particular test.

<br>

Allow with fairly minimal setup, no monkey-patching, and fine-grained control. This is part of a broader pattern in software development: composition over inheritance (`useful Python overview here`).

Hopefully this shows the power and versatility of FastAPI's dependency injection system. learning the value of this approach will save you a lot of pain.

<br>

## Part 12 - Setting Up a React Frontend

<br>

### Theory Section - How Frontends Interact with FastAPI

<br>

So far in this tutorial series we've only interacted with ou API via the Open API (swagger) UI, and by serving a fairly limited Jinja2 template. If your system is all backend microservices, the this is fine. However, if you're looking to serve a more complex frontend the you'll probably want to leverage a modern JavaScript framework like:
- React
- Angular
- Vue

<br>

Whilst each of these frameworks has their pros and cons, their typical interaction with FastAPI is quite similar.

Here is a rough architecture diagram:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/react-fastapi-architecture.png)

<br>

As shown in the diagram, the fundamental way the frontend frameworks interact with the backend is by making HTTP calls via `AJAX`. The typical interface to the backend is a `REST API`.

A variation on this architecture would be a GraphQL approach, but that is not what we will focus on in this post.

You could implement the backend in any language (node, PHP, Java.. any language that can create a web server), but since this is a FastAPI tutorial, the Python choice is made for us.

Since React is the most popular of the modern frontend frameworks, this is the one i have chosen to use for the tutorial series. Whilst isn't a seris on React, i will cover it in enough detail to give a meaningful example of how it would work with FastAPI - so i'm including common requirements like auth, and including multiple pages and components. My idea here is that if you combine this tutorial with other dedicated React tutorials (i recommend the `getting started` docs), you'll be able to put together all the pieces you need for interaction across the full stack.

<br>

Note, we'll look at deployment of both the front and backends later in the tutorial series.

<br>

### Practical Section 1 - Setting Up React Create App

<br>

If you're not familiar with React the i suggest checking out the very approachable docs. The key thing to note here is that the `create-react-app` package we're making use of is an offically supported tool that simplifies React apps:

> Create React App is an officially supported way to create single-page React applications. If offers a modern build setup with no configuration.

<br>

Under the hood, React relies on:
- `webpack`: a static module builder
- `babel`  : A JavaScript compile mainly used to convert ECMAScript 2015+ code into a backwards compatible version of JavaScript)
- `ESLint`: A powerful code linter

Each of these usually requires configuring, and it can be a painful hurdle for those unfamiliar with the ecosystem. `Create React app` basically sets sensible defaults for you so you can skip all that setup. At any point you can call the `eject` command (which is irreversible) and then all the underlying config files are revealed so you can customize them. Given this simplification, it's a great tool for when you are starting out, and it offers flexibility as your app grows in complexity.

#### Setting Up the Project Structure

<br>

You'll notice that in part 12 of our `project repo` we have a new `frontend` directory where all React code will be. To get started, cd into this directory then install the dependencies:
- Note that `create-react-app` requires NodeJS 14+
- Run npm install in the directory where your package.json file is located (this lists our dependencies)
- To start the React app run npm start

<br>

Your app will start, and if you then navigate over to `http://localhost:3000/` you should see this:

`Terminal/CMD Prompt` :

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/react_start_terminal.png)

<br>

`localhost:3000`

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/react_app.png)

<br>

At the moment the recipes are being fetched from an externally running version of our FastAPI app (which is deployed using the method we'll explore in the next part of this tutorial series). This API is specified in our `frontend/config.js` file under the `REACT_APP_API_BASE_PATH` settings. However, to test everything locally we'll want to update this value to be our running backend application: `http://localhost:8001`. Obviously we'll first have to start up our backend app, as we have done in the previous entries in the tutorial series.

<br>

Before we hook up the local backend, let's inspect our frontend structure:

`part-12-react-frontend/frontend/src`

~~~
.
├── App.css
├── App.js
├── client.js
├── components
│         ├── Button
│         │         └── Button.jsx
│         ├── DashboardHeader
│         │         ├── index.jsx
│         ├── Footer
│         │         ├── index.jsx
│         ├── FormInput
│         │         └── FormInput.jsx
│         ├── Idea
│         │         └── index.jsx
│         ├── IdeaTable
│         │         └── index.jsx
│         ├── Loader.jsx
│         ├── Modal
│         │         └── PopupModal.jsx
│         ├── Recipe
│         │         └── index.jsx
│         └── RecipeTable
│             └── index.jsx
├── config.js
├── index.css
├── index.js
├── pages
│         ├── error-page
│         │         └── index.jsx
│         ├── home
│         │         └── index.jsx
│         ├── ideas
│         │         ├── index.jsx
│         ├── login
│         │         └── index.jsx
│         ├── my-recipes
│         │         ├── index.jsx
│         │         └── NotLoggedIn.jsx
│         └── sign-up
│             ├── index.jsx
~~~

<br>

This is a pretty standard structure:
- `pages` are our main "containers" of HTML, representing different pages on the site as the name implies.
- `components` are the building blocks which make up these pages, such as forms, buttons, tables and modals.
- `App.js` is where we set up the routing logic which assigns page React functions to a particular url of the site.

<br>

We'll get to the more advanced parts (like `client,js` a little further on in this post).

#### Sidebar: What is JSX?

<br>

You'll notice that all of our page and component files have a `.jsx` extension. This is called JSX, and it is a syntax extension to JavaScript. The `React docs recommend using it` to describe what the UI should look like. JSX may remind you of a template language, but it comes with the full power of JavaScript.

<br>

#### Sidebar: Wha'ts With All the ClassNames - TailwindCSS

<br>

Within the `.jsx` files we're styling the HTML with `TailwindCSS` (this is what all the `className="flex items-center justify-center`) type of lines are about) which has gained popularity over the past few years due to its ease of use, especially for responsive design.

<br>

#### Sidebar: React Hooks

<br>

`Hooks` were added in `React 16.8`. If you wrote React before this update and you're now looking at this tutorial, you might be wondering where all the React classes are. The answer is: They're not needed if we use hooks.

From `the docs:

> Hooks let you use more of React's features without classes. Conceptually, React components have always been closer to functions. Hooks embrace functions, but without sacrificing the practical spirit of React.

<br>

### Practical Section 2 - Calling FastAPI from the Frontend

<br>

Now that we understand how or React frontend application works, let's have it fetch data from our FastAPI backend.

In `frontend/src/pages/home/index.jsx` We have the following component:

~~~
// code omitted...

const client = new FastAPIClient(config);

const MainView = () => { // [1]
    const [recipes, setRecipes] = useState([]) //[2]

    useEffect(() => {
            fetchEcampleRecipes()
    },[]) //[3]

    const fetchExampleRecipes = () => {
        client.getSampleRecipes('chicken').then((data) => { // [4]
            setRecipes(data?.results) //[5]
        })
    }
    
    return (
        <RecipeTable recipes={recipes} />
    )
}

// code continues...
~~~

<br>

Let's break this down:

1. We define our React `MainView` reusable component as a function (note this is the functional component style, `see this guide` for an overview of the differences vs. class based components)
2. Because we're using functional components, we use `React Hooks` suc as useState
3. We make use of the powerful `useEffect` hook (`docs`), which allows us to perform side effects in function components. Note that the empty array passed in as the second argument indicates this effect will only be called once (this empty array is the default so could be ommited, but i'm including it for clarity).
4. We use our instantiated `FastAPIClient` (more on this soon) to call the backend API. The response data is gathered via `.then` syntax promise chaining. In Javascript there are two main ways to handle asynchronous code: `then/carch` (ES6) and `async/await` syntax, i think it's more useful for backend devs who might not be as up-to-date with modern JS to easily follow along (`see here for a comparison` of the two approaches).
5. We set the recipe data fetched from the API using the state hook.

<br>

Ok, let's go deeper now and lok at what the client `FastAPIClient getSampleRecipes` method is doing:

`client.js`

~~~
// code omitted...
import config from "./config"
const axios = require("axios") //[1]

class FastAPIClient {
    constructor(overrides){
        this.config = {
            ...config,
            ...overrides,
        }

        this.apiClient = this.getApiClient(this.config) //[2]
    }
    /* Create Axios client instance pointing at the REST api backend */
    getApiClient(config){
        let initialConfig = {
            baseURL: `${config.apiBasePath}/api/v1`, //[3]
        }
        let client = axios.create(initialConfig)
        client.interceptors.request.use(localStorageTokenInterceptor) //[4]
        return client
    }

    getSampleRecipes(keyword) {
        return this.apiClient.get(`/recipes/search/?keyword=${keyword}&max_results=10`).then(({data}) => { //[5]
            return data
        })
    }
// code continues...
}
~~~

<br>

1. We use the JavaScript `Axios` promise-based HTTP client, which includes session support we will make use of.
2. We instantiate the `apiClient`, which is an Axios session
3. The `apiBasePath` URL comes from the `config.js` file - for local development this is `http://localhost:8001`, but you'd update it via environment variable for deployment (we'll cover this in the next post in the series). Note that we append the `/api/v1` to match our recipe API structure. All subsequent requests with this client will automatically have this base URL prepended.
4. We make use of Axios request `interceptors` which allow us to update the request headers for auth purposes (more on auth shortly).
5. Using the Axios session we call our `recipes/search?keyword` endpoint and return the response data.

<br>

The recipes/search endpoint should be familiar from previous parts of the tutorial

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/search_endpoint.png)

<br>

In order to see this client working, let's start the backend:
- Follow the setup in the README.md
- Create the DB tables with: poetry run ./prestart.sh
- Start the FastAPI server with poetry run ./run.sh
- Update your frontend/config.js to set REACT_APP_API_BASE_PATH to http://localhost:8001 (note do not use https with localhost)

    ![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/react_app_config.png)

- In a separate terminal/command prompt, start your React app (or if it is already running, refresh the page at `localhost:3000`)

You should now see recipe data:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/react_app.png)

<br>

And if you open up the browser dev tools and look at the network tab, you'll see the app making requests to the backend running at http://localhost::8001:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/dev_tools.png)

<br>

Great! Now let's look at user auth.

<br>

### Practical Section 3 - React Auth with FastAPI and JWTs

<br>

As promised, we're going beyond just a toy example. We'll hook up an auth mechanism between our React frontend and our JWT-based backend auth system which we covered in `part 10`

We'll start with the `/frontend/src/pages/sign-up/index.jsx

We have a pretty standard React registration form, which makes use of our FormInput and Button components located:
- `frontend/src/components/FormInput/index.jsx`
- `frontend/src/components/button/index.jsx

<br>

`sign-up/index.jsx`

~~~
// skipping imports for brevity
const client = new FastAPIClient(config);

const SignUp = () => {
    const [error, setError] = useState({
        email: '',
        password: '',
        fullName: '',
    });
    const [registerForm, setRegisterForm] - useState({
        email: '',
        password: '',
        fullName: '',
    }); //[1]
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate() //[2]

    const onRegister = (e) => {
        e.preventDefault();
        setLoading(true)
        setError(false);

        // skipping form checking for brevity

        client.register(registerForm.email, registerForm.password, registerForm.fullName) //[3]
            .then(() => {
                navigate('/my-recipes') //[4]
            })
            .catch((err) => {
                setLoading(false);
                setError(true);
                alert(err);
            });
    }

    //skipping header for brevity
    return (
        <>
            <form onSubmit={(e) => onRegister(e)}> //[5]
                <FormInput
                    type={"text"}
                    name={"fullName"}
                    label={"Full Name"}
                    error={error.fullName}
                    value={registerForm.fullName}
                    onChange={(e) => setRegisterForm({
                        ...registerForm,
                        fullName: e.target.value,
                    })}
                />
                <FormInput
                    type={"email"}
                    name={"email"}
                    label={"Email"}
                    error={erroe.email}
                    value={registerForm.email}
                    onChange={(e) => setRegisterForm({
                        ...registerForm,
                        email: e.target.value,
                    })}
                />
                <FormInput
                    type={"password"}
                    name={"password"}
                    label={"Password"}
                    error={error.password}
                    value={registerForm.password}
                    onChange={(e) => setRegistrationForm({
                        ...registerForm,
                        password: e.target.value,
                    })}
                />
                <Button 
                    title={"Create Account"} 
                    error={error.password}
                    loading={loading}
                />
            </form>

            {/*Skipping additional code for brevity*/}
    )
}
~~~

<br>

This is pretty standard React code, but for those backend devs who might be a bit rusty, here's quick breakdown:

1. We update the form input fields with the React `useState` hooke
2. The `useNavigate` hook is from the `react-dom-router` library, which is used for routing.
3. We're using our FastAPI client `register` method to call the backend (we'll look at this next)
4. Upon successful registration we navigate to the `/my-recipes` page
5. Standard React from submission code, indicating that we'll call the `onRegister` function when the form is submitted.

<br>

Ok great, next up we'll dig down into the client:

`client.js`
~~~
// within the FastAPIClient class
register(email, password, fullName){
    const loginData = {
        email,
        password,
        full_name: fullName,
        is_active: true,
    }
    
    return this.apiClient.post("/auth/signup", loginData).then(
        (resp) => {
            return resp.data
        }
    )
}
// code continues...
~~~

<br>

Here we prepare all the registration form data gathered in our React component. This `loginData` is then set as the body of a POST request to our API `/auth/signup` endpoint. We return the response (which will be the JWT token). Feel free to play arround with this endpoint yourself by starting up the backend, navigating to the /docs interactive UI and trying it out:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/auth_endpoint.png)

<br>

So now we have registered a user. We still need to login.

The login React page follows almost exactly the same format and logic as the registration page (obviously calling the `login` method on the client instead of the `register` method) so i won't go over that. Where things differ is in the client:

`client.js`

~~~
// within the FastAPIClient class
login(username, password){
    delete this.apiClient.defaults.headers["Authorization"] //[1]

    // Generate form data for submission
    var form_data = new FormData()
    const grant_type = "password"
    const item = {
        grant_type,
        username,
        password,
    }
    for (var key in item){
        form_data.append(key, item[key])
    }

    return this.apiClient
        .post("/auth/login", form_data) //[2]
        .then((resp) => {
            localStorage.setItem("token", JSON.stringify(resp.data)) //[3]
            return this.fetchUser() //[4]
        })
}

fetchUser() {
    return this.apiClient.get("/auth/me").then(({data}) => { //[5]
        localStorage.setItem("user", JSON.stringify(data)) //[6]
        return data
    })
}

// code continues...
~~~

<br>

Lot's happening in this code block, let's break it down:

1. The `Authorization request header` is the key header that must be set correctly for a valid login. We start by deleting it to ensure a stale default value is not used by the session.
2. We POST the login data to the backend `/auth/login` endpoint
3. We store the response (which will be a JWT in the browser `local storage`
4. We're now in possesion of a JWT, and we use that to fetch the user data via the `fetchUser` method.
5. This involves making a GET request to the backend `/auth/me` endpoint.
6. And then we store the response user data in local storage (as well as the token).

`Inspecting Local Storage`:

![](https://christophergs.com/assets/images/ultimate-fastapi-tut-pt-12/user_auth_local_storage.png)

<br>

Every request the React app makes to the backend API has an `Authorization` header inserted via the `localStorageTokenInterceptor` we specified earlier in the `getApiClient` method. Let's look at the interceptor function, which is the final piece in our client-side auth story:

~~~
import jwtDecode from "jwt-decode"
import * as moment from "moment"

// every request is intercepted and has auth header injected.
function localStorageTokenInterceptor(config){
    let headers = {}
    const tokenString = localStorage.getItem("token")

    if (tokenString) {
        const token = JSON.parse(tokenString)
        const decodedAccessToken = jwtDecode(token.access_token) //[1]
        const isAccessTokenValid = moment.unix(decodedAccessToken.exp).toDate() > new Date() //[2
        if(isAccessTokenValid){
            headers["Authorization"] = `Bearer ${token.access_token}` //[3]
        }else{
            alert('Your Login session has expired')
        }
    }
    config["headers"] = headers
    return config
}
~~~

<br>

Key lines to note:

1. We use the `jwt-decode` library to decode the token - note that decoding is not the same as validating which can only be done on the server where the JWT secreet resides (`part 10` goes over JWT theory if you need a refresher)
2. We then check the expiry data of the JWT using the `Moment.js` library (you can use a more modern alternative if you prefer)
3. Finally, we set the `Authorization` header for the request.

<br>

And voila, now requests to our FastAPI endpoints which require user auth are possible. In our React app, this allows us to have the concept of login-required pages. The `pages/my-recipes` page is an example of this. We can set component state based on the presence of a token:

`my-recipes/index.jsx`

~~~
useEffect(() => {
    const tokenString = localStorage.getItem("token")
    if(tokenString){
        const token = JSON.parse(tokenString)
        const decodedAccessToken = jwtDecode(token.access_token)
        if(moment.unix(decodedAccessToken.exp),toDate() > new Date()){
            setIsLoggedIn(true)
        }
    }
}, [])
~~~

<br>

And then display different HTML and/or redirect based on this state. In our example React app the "my-recipes" page is only displayed to logged in users, and attempts to create new recipes for non-logged in users will fail.

We're also able to chain calls to get user information and then create recipes for a specifc user based on the ID (recall, this is how the POST `/recipes/` endpoint is structured, expecting a `submitter_id` as one of the POST body fields):

`my-recipes/index.jsx`

~~~
client.fetchUser().then((user) => {
    client.createRecipe(
        recipeForm.label,
        recipeForm.url,
        recipeForm.source,
        user?.id,
    ).then((data) => {
        fetchUserRecipes()
        setLoading(false)
        setShowForm(false)
    })
})
~~~

<br>

We've mostly considered the frontend additions so far, but we also need to take a moment to look at a few key updates to the API...

<br>


### Practical Section 4 - FastAPI Updates

<br>

#### FastAPI CORS With Frontends (like React)

<br>

CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend running in a browser has JavaScript code that communicates with a backend, and the backend is in a different "origin" than the frontend.

Quoting from the `docs`:

> So, let's say you have a frontend running in your browser at `http://localhost::8080`, and its JavaScript is trying to communicate with a backend running at `http://localhost`(because we don't specify a port, the browser will assume the default port 80). Then, the browser will send an HTTP OPTIONS request to the backend, and if the backend sends the appropriate headers authorizing the communication from this different origin (`http://localhost:8080`) then the browser will let the JavaScript in the frontend send its request to the backend. To achieve this, the backend must have a list of "allowed origins".

<br>

In short, this gives you control over which frontends can call your API, which is often useful. In the case of our Recipe API and React frontend, we do need to allow some origins to call our API, such as localhost (for local development) and our deployed frontend application.

We do this in two places. The first is by using the FastAPI CORS Middleware. We add this to `main.py` like so:

`backend/app/app/main.py`

~~~
# Skipping a few import for brevity
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.moddleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

root_router = APIRouter()
app = FastAPI(title="Recipe API", openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
# Code Continues
~~~

<br>

Above, when `BACKEND_CORS_ORIGINS` is set in our settings, then the CORS Middleware is applied, and the `allowed_origins` are set via a list comprehension on the `BACKEND_CORS_ORIGINS` value. This brings us to the second update, which is introducing this setting:

`backend/app/app/core/config.py`

~~~
# Skipping import for brevity

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8001", # type: ignore
        "https://fastapi-recipe-app.herokuapp.com"
    ]
# Code continues...
~~~

<br>

Notice how `BACKEND_CORS_ORIGINS` includes both localhost and our deployed frontend application (on Heroku). We'll be looking at the Heroku deployment in the next part of the tutorial. Wherever you deploy your frontend, you'll need to update this value to reflect it. Once the value is set correctly, you'll be able to call your API without any CORS erros.

Phew! That was a lot of information. But now we have a truly modern frontend to interact with our FastAPI backend. Now we need to deploy everything.. that's coming up next.

























