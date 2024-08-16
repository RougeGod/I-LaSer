# LaSer - Language Server

## Introduction

LaSer answers users' algorithmic questions about regular languages. For example, given a regular language L, LaSer can decide whether L satisfies a certain property, whether L is maximal with respect to a certain property, and construct languages that satisfy a certain property.

It can compute the edit distance of L, as well as some other examples.

## File Structure

```
app/
  templates/ - contains html templates for the given pages of LaSer
    tabs/ - contains static HTML files corresponding to the non-interactive pieces of the website
  testing/ - contains tests and test files for LaSer Unit Testing
  transducer/ - contains the bulk of the site, including the views and handlers that integrate with FAdo.
laser/ - contains configuration files for the server.
  apache_settings/ - contains configuration files
media/ - contains the output when programs are generated using LaSer - more on this later
static/ - contains the static css/js files that help run the webpage
  css/ - css files
  js/ - js files
```

## Important Files

### `app/transducer/views.py`

Contains the interface between the django frontend and the actual logic behind LaSer. It also currently contains the get_code method, which handles code generation.
`
### `app/transducer/handlers.py`

Contains the methods that handle `get_response` - that is, the code that parses the user's input choices into automata. Importnatn methods in handlers.py include: 

- `handle_construction`
- `handle_iap`
- `handle_ipp`
- `handle_approximate_maximality`


#### `handle_construction`

This method handles language construction. It can handle fixed properties on its own. It uses two other methods, `handle_iap` and `handle_ipp` to handle more complex properties.

#### `handle_iap`

`handle_iap` is the method that handles language construction for input-altering properties. If the calculation is too large for the server to handle, it fails and alerts the user to generate the necessary python code to run it.

#### `handle_ipp`

`handle_ipp` is the method that handles language construction for input-preserving properties. If the calculation is too large for the server to handle, it fails and generates the necessary Python 3 code for the user to run

#### `handle_satisfaction_maximality`

`handle_satifaction_maximality` handles, jointly (due to their similarity) questions of satisfaction, maximality, and approximate maximality of languages with repsect to a given property. This method is very large, but is difficult to split up due to its reliance on many local variables and the similar code that all three questions share. a refactor of this method will eventually be necessary.

### `app/transducer/laser_gen.py`

This file handles code generation for when the user wants to run the python program on their local machine instead of through the website. this is required if the question that is being asked is too computationally expensive to run.

It contains methods that are used to generate the code for the local running of a question.

## Running Unit Tests

In order to run the python unit tests, navigate to the root of the directory and run `python manage.py test`. This will tell django to run all the unit tests in the project.
