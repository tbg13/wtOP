# What the One Piece ??

The goal of this project is to learn, train and showcase the 2 main skills Data Engineers should know in my opinion:
1) Setting up stuff to hold data
2) Doing stuff to the data itself

The first point is all about infrastructure : api management, databases, self-service analytics, etc.

The second point is about the data itself : extracting, loading, transforming, cleaning, checking, validating, duplicating, managing workflows ...

The following project has 3 modules for the time being:
1) Extracting : scrapping and API
2) Loading & Transforming : moving data, databases, SQL transformations, workflow orchestration, ...
3) Exposing : self-service analytics, webapp

The technical stack is as follows:
- Extracting :
    - scrapping > beautiful soup
    - API > fastAPI
- Loading & Transforming
    - moving data > custom connectors using Python classes (OOP)
    - databases > bronze/silver in minIO and gold in DuckDB
    - SQL transformations > dbt ran on top of DuckDB engine
    - workflow orchestraction > dagster

- Infrastructure > docker (custom images)
- Version control > git
- CI/CD > TBD

- Development > Linux, Python

Check old_readme.md for more informations (slightly outdated) !

What I'd like to add in the future once mvp running:
- streaming data
- spark (scala or py ?)
- validation/data contract > pydantic (?)

What I'd like to do more:
- another api>dbt workflow
- more api calls 