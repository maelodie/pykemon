# PALLET TOWN : A PYKEMON GAME

## DESCRIPTION
This Python-based project, powered by the Pygame library, creates a dynamic life simulation in a Pokémon-themed environment, in the context of the LU2IN013 teaching unit at Sorbonne University about project development using SCRUM methods. Key features include:
- Customized map with forests, lakes, villages, and islands using Tiled
- Character movement with a centered camera for an immersive experience.
- Pokémon with distinct types: Fire (tree igniting), Water (water traversal), Poison (poisoning).
- Evolutionary system for Pokémon, including fleeing and hunting mechanisms.
- Forest fires triggered by fire-type Pokémon, spread using Moore's neighborhood.
- Rain and drought system affecting lakes, with flood prevention during heavy rain.
- Day and night cycle triggered manually (D/N keys) or automated.
- Temperature display indicating long-term changes in simulation time.
- Combat mode allowing the character to face and defeat Pokémon.

A detailed explanation about the aims of the project is included in /docs.

## INSTALLATION
To install the project:
- Clone the repository
- Execute this line of code in the terminal, after in the src folder:
```
python3 main.py
```
**Required libraries: pytmx, pygame**

## USAGE
Feature keys are:
- 'D': Force day mode
- 'N': Force night mode
- 'R': Activate rain
- 'T': Deactivate rain

## SOURCES
**Sprites**: 
https://www.spriters-resource.com

**Coding tutorials**: 
- https://github.com/clear-code-projects/PyDew-Valley
- https://github.com/RubenPain/Python-Pokemon-with-Pygame

## CONTRIBUTORS
Special thanks to the following individuals with whom I've worked with for this project: 
- [Jules MAZLUM](https://github.com/julesmazlum)
- Eva Farin-Reis VIEGAS
