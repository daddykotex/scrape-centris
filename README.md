Project to scrape Centris real estate listing.

## Requirements

1. direnv
2. pyenv

## Getting started

When you move into the directory, `direnv` will automatically load the `.envrc` file and set configure your shell with everything you need to run the project.

If this is the first time you hop into the directory, you will need to run `direnv allow` to allow the shell to run the project.

If you don't have `direnv` installed, you can manually install the right python version and the right poetry version.

Then you'll need to install the dependencies, for that, you can run: `poetry install --no-root`.

## Running the project

Scrapy is used to load the data from Centris.

You can do: `scrapy crawl centris-plex -O results.json` to run the scraper.

## Resources

See: https://github.com/hussnainsheikh/centris-scraper
