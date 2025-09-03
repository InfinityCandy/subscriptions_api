## Project Setup

Each one of the steps described below contains the commands that need to be run in order to complete the configuration step.

This guide assumes that you already have PostgreSQL installed and configured and that you have already created a Schema for your Django project and one User for that Schema and that the default DB in the Django project is PostgreSQL.

1. Navigate to project's root folder:

```
$ cd subscriptions_api
```

2. Create a new virtual environment:

```
$ python -m venv .venv
```

3. Activate virtual environment:

```
$ source .venv/bin/activate
```

4. Install project dependencies:

```
$ pip install -r requirements.txt
```

5. Copy the .env file containing the env variables into a new file:

```
$ cp .env.template .env
```

6. Setup env variables:

```
SECRET_KEY=
```

You can generate a new secrete to be used as your secrete key by running the following commad in a new terminal:

```
$ python

>>> import secrets
>>> secrets.token_hex(16)
```

7. Run migrations:

```
$ flask db upgrade
```

8. Run the following script to populate the SubscriptionsPlan table

```
$ flask shell

>>> from scripts.populate_subscription_plans import populate_subscription_plans
>>> populate_subscription_plans()
```

## Optimizations Stategies

- Relationships Lazy Load: The argument "lazy=True" was used when defining relationships between models, so, only when explicitly calling the other end of the relationship the records associated to this model are going to be loaded, otherwise it will only load the main model.
- Raw Queries: Using raw queries that where directly sent to the DB instead of calling the ORM it's a recommended strategy to improve the speed of any query.
- Soft Deletes: Marking Subscriptions as inactive is another strategy to prevent slow queries from happening, because, instead of going directly to the DB and deleting a whole record or set of records from disk, the only change that is made is flipping a value in the DB.
- Indexing: Another recommended stategy that was used was the use of indexes for the "active" column in the Subscriptions model. The idea of this was to speed up the look of active an inactive Subscriptions by helping sqlite to look at a table of indexes associated to this column (This is done under the hood by simply sending the RAW to sqlite)
- Keep Models Simple: In order to prevent any unecessary optimization the models where kept as simple as possible to avoid creating slow queries
