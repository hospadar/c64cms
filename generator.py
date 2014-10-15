from __future__ import print_function
import os, markdown, codecs, re, shutil
from jinja2 import Environment, FileSystemLoader

def remove_ext(filename):
    parts = filename.split(".")
    if len(parts) > 1:
        return ".".join(parts[0:-1])
    else:
        return filename

def build_map(in_path, base_path, level=0):
    """
    Iterate through source dir and build out the map
    Only looks for markdown files (looks for .md extension)
    """
    
    output = {"type":"category", "contents":{}}
    md = markdown.Markdown(output_format = "html5", extensions = ['markdown.extensions.meta'])
    
    for thing in os.listdir(in_path):
        if os.path.isdir(os.path.join(in_path, thing)):
            children = build_map(os.path.join(in_path, thing), base_path, level=level+1)
            if len(children["contents"]):
                output["contents"][thing] = children
        elif thing.endswith(".md"):
            current_file = {}
            current_file["content"] = md.convert(codecs.open(os.path.join(in_path, thing), encoding="utf-8").read())
            current_file["slug"] = re.sub("\W+", "-", remove_ext(os.path.basename(thing)))
            current_file["title"] = " ".join(md.Meta.get("title", [])) or current_file["slug"]
            current_file["template"] = "".join(md.Meta.get("template", [])) or "default.html"
            current_file["input_path"] = os.path.join(in_path, thing)
            current_file["output_path"] = os.path.join(os.path.relpath(in_path, base_path), current_file["slug"] + ".html")
            current_file["level"] = level
            current_file["menu"] = " ".join(md.Meta.get("menu", [])) or current_file["title"]
            current_file["type"] = "page"
            output["contents"][thing] = current_file
    
    return output


def render_map(site_map, menu, out_path, template_dir):
    """Render the site map"""
    for name, page in site_map["contents"].items():
        if page["type"] == "category":
            render_map(page, menu, out_path, template_dir)
        elif page["type"] == "page":
            env = Environment(loader = FileSystemLoader(template_dir))
            template = env.get_template(page["template"])
            page_dir = os.path.join(out_path, os.path.dirname(page["output_path"]))
            if not os.path.exists(page_dir):
                os.makedirs(page_dir)
            outfile = codecs.open(os.path.join(out_path, page["output_path"]), "w", encoding="utf-8")
            outfile.write(template.render(
                page = page,
                menu = menu
                ))
            

    

def copy_everything_else(in_path, out_path):
    for directory, x, files in os.walk(in_path):
        for f in files:
            if not f.endswith(".md"):
                if not os.path.exists(os.path.join(out_path, os.path.relpath(directory, in_path))):
                    os.makedirs(os.path.join(out_path, os.path.relpath(directory, in_path)))
                shutil.copy2(os.path.join(directory, f), os.path.join(out_path, os.path.relpath(directory, in_path), f))
        
    
            

def generate(in_path, out_path, template_dir):
    if os.path.exists(out_path):
        shutil.rmtree(out_path)
    site_map = build_map(in_path, in_path)
    render_map(site_map, site_map, out_path, template_dir)
    copy_everything_else(in_path, out_path)
    
    