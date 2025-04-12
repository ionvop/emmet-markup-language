import flask
import emmet
import os
import bs4


app = flask.Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path: str) -> str:
    path = path.rstrip("/")

    if os.path.isfile(f"src/routes/{path}/index.ehtml") == False:
        return flask.abort(404)
    
    ehtml = open(f"src/routes/{path}/index.ehtml").read()
    ehtml = flatten(ehtml)
    ehtml = emmet.expand(ehtml)
    document = bs4.BeautifulSoup(ehtml, "html.parser")

    if os.path.isfile("src/style.ecss"):
        ecss = open("src/style.ecss").read()
        ecss = parse_ecss(ecss)
        style_tag = document.new_tag("style")
        style_tag.string = ecss
        document.head.append(style_tag)

    if os.path.isfile("src/script.js"):
        script = open("src/script.js").read()
        script_tag = document.new_tag("script")
        script_tag.string = script
        document.body.append(script_tag)

    if os.path.isfile(f"src/routes/{path}/style.ecss"):
        ecss = open(f"src/routes/{path}/style.ecss").read()
        ecss = parse_ecss(ecss)
        style_tag = document.new_tag("style")
        style_tag.string = ecss
        document.head.append(style_tag)

    if os.path.isfile(f"src/routes/{path}/script.js"):
        script = open(f"src/routes/{path}/script.js").read()
        script_tag = document.new_tag("script")
        script_tag.string = script
        document.body.append(script_tag)

    output = document.prettify()
    return output


def parse_ecss(ecss: str) -> str:
    output = ""
    abbr = ""
    i = 0

    while i < len(ecss):
        char = ecss[i]

        if char == "{":
            abbr = abbr.strip()
            output += f"{abbr}{{"
        elif char == "}":
            output += "}"
        elif char == ";":
            abbr = abbr.strip()

            if abbr[0] == "-":
                abbr += ";"
            elif abbr[0] == "_":
                abbr = abbr[1:] + ";"
            else:
                abbr = emmet.expand(abbr, {"type": "stylesheet"})
            output += abbr

        abbr += char

        if char in "{};":
            abbr = ""

        i += 1

    return output


def flatten(ehtml: str) -> str:
    ehtml = ehtml.splitlines()
    output = ""

    for line in ehtml:
        line = line.strip()

        if "~" in line:
            include_path_start = line.find("~")
            include_path_end = line.find(";", 1)
            include_path = line[include_path_start + 1:include_path_end]

            if os.path.isfile(f"src/{include_path}.ehtml"):
                include = open(f"src/{include_path}.ehtml").read()
                output += line[:include_path_start] + flatten(include) + line[include_path_end + 1:]
        else:
            output += line

    ehtml = "".join(output)
    return ehtml


if __name__ == "__main__":
    app.run()