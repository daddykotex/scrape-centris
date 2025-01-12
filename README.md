Project to scrape Centris real estate listing.

## Requirements

1. nix
2. direnv *

## Getting started

When you move into the directory, `direnv` will automatically load the `.envrc` file and set configure your shell with everything you need to run the project.

If this is the first time you hop into the directory, you will need to run `direnv allow` to allow the shell to run the project.

If you don't have `direnv` installed, you can do `nix develop` once you're in the directory to get the same effect.

Then you'll need to install the dependencies, for that, you can run: `poetry install --no-root`.

## Running the project

You can do: `poetry run python -m sample_package` to run the project.

## Resources

See: https://github.com/hussnainsheikh/centris-scraper
