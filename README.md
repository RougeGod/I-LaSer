# LaSer - Language Server

## Introduction

LaSer answers users' algorithmic questions about regular languages. For example, given a regular language L, LaSer can decide whether L satisfies a certain property, whether L is maximal with respect to a certain property, and construct languages that satisfy a certain property.

It can compute the edit distance of L, as well as some other examples.

## File Structure

```
app/
  templates/ - contains html templates for the given pages of LaSer
    upload.html - the main HTML page with all of the interactivity of I-LaSer
    tabs/ - contains static HTML files corresponding to the non-interactive pieces of the website
  testing/ - contains tests, testing utilities, and test files for LaSer unit testing
  transducer/ - contains the bulk of the site, including the views and handlers that integrate with FAdo.
laser/ - contains configuration files for the server. (private)
localversion/ - contains the code for the executable (Linux) program, the Windows program is extremely similar
    /laser - similar to the app/transducer folder, contains all backend calculation methods
media/ - contains the output when programs are generated using LaSer and the downloadable executables
static/ - contains the static css/js files that help run the webpage
  css/ - css files
  js/ - js files
```

## Important Files

### `app/transducer/views.py`

Contains the interface between the django frontend and the actual logic behind LaSer. It also currently contains the get_code method, which partially handles code generation. Function timeouts are also in here, stopping calculations that take longer than 15 seconds. The GUI in localversion/laser does not use views.py
`
### `app/transducer/handlers.py`

Contains the methods that handle `get_response` - that is, the code that parses the user's input choices into automata and calculate the answer to the query on the server. Important methods in handlers.py include: 

- `handle_construction`
- `handle_iap`
- `handle_ipp`
- `handle_satisfaction_maximality`
- `check_approximate_maximality`
- `check_satisfaction`


#### `handle_construction`

This method handles language construction. It can handle fixed properties on its own. It uses two other methods, `handle_iap` and `handle_ipp` to handle more complex properties.

#### `handle_iap`

`handle_iap` is the method that handles language construction for input-altering properties. If the calculation is too large for the server to handle, it fails and generates the necessary Python code for the user to run.
#### `handle_ipp`

`handle_ipp` is the method that handles language construction for input-preserving properties. If the calculation is too large for the server to handle, it fails and generates the necessary Python code for the user to run.

#### `handle_satisfaction_maximality`

`handle_satifaction_maximality` handles, jointly (due to their similarity) questions of satisfaction, maximality, and approximate maximality of languages with repsect to a given property. This method is very large, but is difficult to split up due to its reliance on many local variables and the similar code that all three questions share. A refactor of this method will eventually be necessary. If the calculation parameters are too large, it will fail and generate the Python program.

#### `check_approximate_maximality`

`check_approximate_maximality` contains the functionality specific to approximate maximality, checking the parameters and doing the approximate maximality calculation.

#### `check_satisfaction`

`check_satisfaction` contains functionality specific to the satisfaction question, which is also required for approximate maximality. 

### `app/transducer/laser_gen.py`

This file handles code generation for when the user wants to run the python program on their local machine instead of through the website, or if the function cannot be calculated on the server. Code generation is required if the question that is being asked is too computationally expensive to run or takes too long on the server.

It contains methods that are used to generate the code for the local running of a question.

### `app/transducer/laser_shared.py`, `app/transducer.util.py`

These files both handle backend methods used across LaSer.

### `app/transducer/expand_carets.py`

This file handles the expansion of regular expressions which use the caret (^) operator to repeat parts of strings.

### `localversion/ilaser-gui.py`

This file contains all code for the frontend and interactivity of the GUI program. Calculations are handled in `localversion/laser` with the same files as `app/transducer`.

## Running Unit Tests

In order to run the python unit tests, navigate to the root of the directory and run `python manage.py test`. This will tell django to run all the unit tests in the project.

##Further Reading

The file /localversion/manual.pdf contains detailed property descriptions and formatting instructions. While the manual is tailored specifically for the local GUI, the web version and the GUI are very similar, so the instruction manual is still useful even for users of the web version who never touch the GUI.
