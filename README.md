# Kumir-Compose

A preprocessing and package management tool for modern 
Kumir development.

## Prerequisites
Install a Kumir SDK first ([niisi.ru](https://www.niisi.ru/kumir/dl)).

This project was tested only on Windows. It should
work on other systems too, but it's not guaranteed.

## Installation
```sh
pip install kumir-compose
# requires python 3.12+
```

## Usage
Create a Kumir-Compose project:
```sh
$ kumir-compose init
Enter project name: test project
Select library directory [lib]: 
Do you want Kumir-Compose to automatically find Kumir SDK [Y/n]? Y
Config created.
```

Download a dependency:
```sh 
$ kumir-compose depend k-collections
```

Run the project:
```sh
$ kumir-compose run main.kum
```

## Configuration file:
```yaml
# Project config
project:
  
  # Name of the project
  name: example project
  
  # Dependencies list
  # Default: empty list
  depends:
    k-collections: latest
    
  # Directory to store dependencies
  library_location: lib  # default
  
  # Where to search for files for inclusion
  lookup:
    - lib  # default
    
  # How to name assembled files
  filename_format: %s.kum  # default
  
  # List files for distribution.
  # They will be downloaded upon requesting your project
  # as a dependency for other project.
  # Default: empty list
  distribute:
    - my_lib.kum


# Kumir-Compose settings
settings:
  
  # SDK binary paths
  sdk:
    compiler: 'C:\\\\Program Files (x86)\\\\Kumir-2.1.0-rc11\\\\bin\\\\kumir2-bc.exe'
    release: 'C:\\\\Program Files (x86)\\\\Kumir-2.1.0-rc11\\\\bin\\\\kumir2-xrun.exe'
    debug: 'C:\\\\Program Files (x86)\\\\Kumir-2.1.0-rc11\\\\bin\\\\kumir2-xrun.exe'
```

## Preprocessor

Preprocessor defines following directives:
- `|| include "path/to/file"` = `|| включить "путь/к/файлу"`
  <br>
  Every file is included only once.
- `|| ifdef MACRO` = `|| еслизад МАКРОС`
- `|| ifndef MACRO` = `|| еслинезад МАКРОС`
- `|| define MACRO ...` = `|| задать МАКРОС ...`
- `|| undef MACRO` = `|| забыть МАКРОС`

## Dependencies

Dependencies are searched in GitHub repositories. 

If name has no slash in it, `kumir-compose` organisation
will be searched.

Examples:
```sh
$ kumir-compose depend k-collections
$ kumir-compose depend my-profile/my-library
$ kumir-compose undepend my-profile/my-library
```

## Licensing

This work is licensed under GNU GPL v3.0

## Author

[@Tapeline](https://github.com/Tapeline)
