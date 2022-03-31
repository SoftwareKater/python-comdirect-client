# Roadmap

- split cli.py into different modules based on the resources
- 'api commands' seem to have the same structure:
  - create session -> create service -> call service -> transform response -> print response
  - make a class / function providing that flow on an abstract level