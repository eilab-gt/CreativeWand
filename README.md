# Creative Wand

This repository holds the implementation of the `Creative Wand` framework, along with an exemplar implementation in text
domain.
For more details on what this is, feel free to check [PAPER LINK].

# Installation & Setup

## Use this as a library

- Create a conda environment using provided `conda_env.yaml`:
    - `conda env create -f conda_env.yml`
    - `conda activate creative-wand`
- `pip install -e .` and you will have `CreativeWand.Framework` available in your workspace.

## Try the exemplar application

- Create a conda environment using provided `conda_env.yaml`:
    - `conda env create -f conda_env.yml`
    - `conda activate creative-wand`
- (Optional) Install apex library (Needed for loading models in half precisions (conserve memory):
  https://github.com/NVIDIA/apex
- Set up Addons
    - Clone https://github.com/eilab-gt/plug-and-blend-tool into `Addons/PNB` and rename the folder `pnb2` (Or
      change `endpoint.py` accordingly)
    - Check `AddonConfig.py` and change paths accordingly
        - Download https://storage.googleapis.com/sfr-gedi-data/gedi_topic.zip , unzip it somewhere and
          point `gedi_location` there;
        - for `base_location` input a desired `huggingface` `gpt2`-compatible model (either a model name or a path to
          given model), or use `gptj` following the config sample.
        - We used `gptj` for our experiments, which requires a lot of VRAM. all functions work with any `gpt`-compatible
          models, although what is generated will be different.
- Additional information on Addons
    - `Addons` are individual modules fulfilling functionalities for our exemplar instantiation.
    - For your convenience, we built a simple REST API framework that can load these moduels, located
      at `CreativeWand.Addons`.
    - Check `Sample.py` for an example Addon.

## Running the exemplar application

In `scripts` folder, run all scripts that start with `start`:

- `start_addon_server.sh` starts addon server;
- `start_experiments_server.sh` starts backend server;
- `start_web_frontend_server.sh` starts the Web interface server.
- Based on your system setup, you may need to `chmod +x [script name]` all scripts, or additionally deal with `node.js`
  dependencies.

# Have fun!
Feel free to open an issue if you get into any problems :) .