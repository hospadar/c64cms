###C64 CMS

Extremely simple static site generator designed to render some markdown files and copy your static stuff to an output directory.
Looks for markdown files (with ".md" extensions) in the source dir, renders them to html in the output dir, copying any other files it finds.

The default style is commodore 64 themed! Yay!

Uses jinja2 templates to handle the rendering.

Check it out in action at [hospadaruk.org](http://hospadaruk.org/)

Reqires jinja2, Markdown, and watchdog.  Should work fine in python 2 or 3
```bash
sudo pip install jinja2 Markdown watchdog
```

2 Python files:

- generator.py: does the actual site generation logic
- build.py: main class, run python build.py -h for help

```bash
$ python build.py -h
usage: build.py [-h] [-d] [-p PORT] [-t TEMPLATE_DIR] [in_path] [out_path]

positional arguments:
  in_path               input directory
  out_path              output directory

optional arguments:
  -h, --help            show this help message and exit
  -d, --dev-server      Run dev server instead of just generating output
  -p PORT, --port PORT  port for dev server
  -t TEMPLATE_DIR, --template-dir TEMPLATE_DIR
                        Directory to find templates
                        
#run development server on port 8080 with default input and output dirs
$ python build.py -d -p 8080
```

Commodore-izing images:
```bash
convert in.jpg -scale 200x200 -monochrome -fill '#A5A5FF' -opaque white -fill '#4242E7' -opaque black  out.jpg
```