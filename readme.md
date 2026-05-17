# Blog Source

My blog is generated using Pelican.
Pelican is a static-site generator, which means that
I write blog posts in markdown files and Pelican uses those files to generate a blog website for me.

This repository contains:

* My blog posts in markdown. These are located in the directory `content`.
* Settings for Pelican in `pelicanconf.py`.
* My pelican plugin for customizing the site-generation process, located in `plugins/my_plugin`.


### Generating a site from source

* Install dependencies:

      python3 -m venv blogVenv
      source blogVenv/bin/activate
      pip install -r requirements.txt

* Install [`dot`](https://graphviz.org/download/) and [`ffmpeg`](https://ffmpeg.org/).

* Get a pelican theme (like [MFPelicanTheme](https://github.com/sharmaeklavya2/MFPelicanTheme)).
  Place the theme's directory at `theme` or create a symlink.

* To generate the blog for local testing, run `make local`.
  The website will be generated in the directory `output`.
  (`output` can be a pre-existing symlink.)
  Then serve the contents of `output` using an HTTP server like [`nginx`](https://nginx.org/) or
  Python's [`http.server`](https://docs.python.org/3/library/http.server.html#command-line-interface).
