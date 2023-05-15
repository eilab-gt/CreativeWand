# Creative Wand

This repository holds the implementation of the `Creative Wand` framework, along with an exemplar implementation in text
domain.
For more details on what this is, feel free to
check [Creative Wand: A System to Study Effects of Communications in Co-Creative Settings](https://ojs.aaai.org/index.php/AIIDE/article/view/21946).

(Please see the `release` branch for the older version of Creative Wand with the framework and the exemplar application unseparated.

# See this in action
See https://github.com/eilab-gt/beyond-prompts-experiment for a storytelling artifact created with Creative Wand. Enjoy!

# Installation & Setup

This is a library that supports applications that is developed using Creative Wand.

## Use this as a library

To set this repository up:

- Set up Creative Wand
  - Create a conda env / virtual env / your favourite
  - Clone the Creative Wand framework (this repo)
  - `cd` to the root of the cloned repository
  - `pip install -e .`
    - Now you will have `CreativeWand` available as a package!

## Information on `Addons`

We provide a simple `flask`-based server implementation for setting up your own
remote REST API (e.g. LM inference, services, etc.).

Check `CreativeWand.Addons.Webserver.AddonServer.run_addon_server()` for more details.

# Have fun!

Feel free to open an issue if you get into any problems :) .
