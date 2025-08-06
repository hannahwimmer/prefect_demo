# Short intro to workflow management

### 0 - Prerequisites

*Everybody should have:*
- Python (ideally 3.12-3.14) installed
- Poetry installed (for package management)


### 1 - Setting up a Poetry environment

Let's start with setting up a proper environment using Poetry (package management tool):
- `poetry init`: initializes Poetry for our project (writing a `.toml` file with basic info about our project)
- `poetry add <package name>`: adds a specific package (e.g., numpy) to our environment
(will update or create a `.lock` file, if it doesn't exist already)
- to add prefect, use `poetry add "prefect[cli]`"
- if there are dependency issues, resolve them in the `.toml` file and save, then try
to add the package again
- `poetry shell`: starts the virtual environment

**Some more relevant commands you might need using Poetry**
- `deactivate` and `exit` to exit to exit a Poetry shell
- `poetry show`: command to view the packages in our environment
- `poetry remove <package name>`: removes a specific package from our environment

### 2 - setting up normal Python code to do what we want

Nice workflow management tool let themselves be integrated smoothly with existing
Python code, so we'll first write the necessary functions to do what we want to do,
and then convert everything to `Prefect` structures later on.

*To recap, we want to:*
- load a PDF form file to Python
- process the structured information there
- summarize or translate that information in some way
- write everything into a "database" (csv-file)

### 3 - managing our workflow with Prefect

To automatize our pipeline (i.e., run it automatically every five minutes or something..)
we're going to use **Prefect**, a workflow management tool. 

**Convert classical Python code to Prefect**
Python code can be converted easily to follow the Prefect structure by adding `@task`
and `@flow` decorators above your functions.

**Log into the Prefect Cloud**
We're going to use the Prefect Cloud (to avoid painful local setups for deploying our
workflow locally). Run:

- `prefect cloud login` (allows you to login for free via GitHub). If it's the first
login, you may need to choose a workspace name and prefect handle. If everything works,
you'll be authenticated and you'll get a terminal message like:

"Authenticated with Prefect Cloud! Using workspace <workspace_name>'"

*Some practical commands:*
- `prefect --help`: returns all the possible commands and options
- `prefect cloud workspace ls`: lists all available workspaces
- `prefect cloud workspace set`: sets the current workspace

**Initializing the Prefect project (generate a deployment configuration)**
To generate a template `.yaml` file that holds the basic configurations for our project,
run:

- `prefect init` (this creates a `.yaml` file with the project specifics). You'll be
asked to select a specific 'deployment configuration recipe' - we'll use 'local',
meaning that the relevant code is just going to be stored on your local PC.

**Create a "work pool"**
In the Prefect UI, we have to create a new work pool, where our deployments will run.
In the free tier, we only have the Prefect Managed work pool option.

- Go to the Prefect UI
- Select `Work pools` > `Create work pool`
- Select the `Prefect Managed` option (the work pool type is then going to be
`prefect:managed`, meaning we do not need to run a local worker; Prefect will manage the
infrastructure)
- Give your work pool a name > create everything with the default settings

For other tiers, you can do this in the terminal via
`prefect work-pool create '<work_pool_name>'`, but in the free tier, you have to use the
UI... 

Once that is done, you can find the work pool via your terminal using:
- `prefect work-pool ls`: lists all the available work pools (only 1 for free tier...)

**Modifying the deployment configuration**
We want to give our deployment and flow a name, and to set up a specific interval at
which the code should be run. We also have to set the work pool to the one we just
created. **Importantly**, we also have to set an **entrypoint**.
This is a path to the relevant script that should be executed, and the function in the
script that should be called at the specified intervals!

**Create a deployment for our project**
We'll create a deployment to deploy a specific flow from our project (in our case,
we want to automatically run the process_pdfs() flow every five minutes). To set that
up, run:

- `prefect deploy`: lets you choose a deployment configuration (in our case, the
deployment corresponding to the `.yaml` file called "folder-watcher"), then lets you
chose a specific flow to deploy (in our case, the flow corresponding to the function
"process_pdfs").

