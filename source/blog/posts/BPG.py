###################################################
#  Chloe's Blog Post Generator - Markdown to HTML #
###################################################

# NOTE: Formatting is ugly, however, it's functional.
# NOTE: I intend to fix all type hints... eventually.

import argparse
from argparse import Namespace
from datetime import datetime
import markdown
from pathlib import Path
import re
from typing import Dict, List

class Generator:
    def __init__(self, markdown_file_path: Path):
        self.markdown_file_path: Path = markdown_file_path

        self.blog_post_data: Dict[str, str] = {
            "post_id": "",
            "post_title": "",
            "post_description": "",
            "publication_date": "",
            "post_content": ""
        }

        self.file_name: str = ""


    def set_blog_post_data(self) -> bool:
        # Set the publication date.

        current_time_utc = datetime.utcnow()

        formatted_time_utc = current_time_utc.strftime("%d %B %Y at %H:%M (UTC)")

        self.blog_post_data["publication_date"] = formatted_time_utc

        # Get the contents of the markdown file.

        try:
            with open(self.markdown_file_path, "r", encoding="utf-8") as markdown_file:
                markdown_file_contents: str = markdown_file.read()
        except FileNotFoundError: # If the file is not found.
            print(f"[-]: {self.markdown_file_path} could not be found.")
            return False
        except IsADirectoryError: # If the path leads to a directory.
            print(f"[-]: {self.markdown_file_path} is a directory.")
            return False
        except PermissionError: # If lacking permission to open/read from the file.
            print(f"[-]: Permission to open or read from {self.markdown_file_path} was denied.")
            return False
        except OSError: # If a general operating system related error occurs.
            print(f"[-]: Generic OS error occurred whilst attempting to open and read {self.markdown_file_path}.")
            return False

        # Identify content elements (ID, title, description, body).
        pattern = r"-!\s(\d+)\n-!\s([^\n]+)\n-!\s([^\n]+)(.*)"

        # Match the content elements defined by the pattern above.
        match = re.search(pattern, markdown_file_contents, re.DOTALL)

        if match:
            self.blog_post_data["post_id"] = match.group(1)
            self.blog_post_data["post_title"] = match.group(2)
            self.blog_post_data["post_description"] = match.group(3)

            markdown_content = match.group(4).strip() # Markdown content (Line 5+).

            self.blog_post_data["post_content"] = markdown.markdown(markdown_content, extensions=["fenced_code", "tables"])

            print(self.blog_post_data["post_content"])
        else:
            print(f"[-]: {self.markdown_file_path} is improperly formatted; please validate the metadata section.")
            return False

        return True


    def generate_blog_post(self) -> bool:
        html_document: str = f"""\
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <!-- Meta -->
                <meta charset="UTF-8">
                <meta name="referrer" content="no-referrer">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">

                <!-- Description -->
                <meta name="description" content="{self.blog_post_data["post_description"]}">

                <!-- Style Sheets -->
                <link rel="stylesheet" href="../../styles.css">
                <link rel="stylesheet" href="posts.css">

                <!-- FontAwesome -->
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">

                <!-- KaTeX -->
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css" integrity="sha512-fHwaWebuwA7NSF5Qg/af4UeDx9XqUpYpOGgubo3yWu+b2IQR4UeQwbb42Ti7gVAjNtVoI/I9TEoYeu9omwcC6g==" crossorigin="anonymous" referrerpolicy="no-referrer" />

                <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js" integrity="sha512-LQNxIMR5rXv7o+b1l8+N1EZMfhG7iFZ9HhnbJkTp4zjNr5Wvst75AqUeFDxeRUa7l5vEDyUiAip//r+EFLLCyA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
                <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js" integrity="sha512-iWiuBS5nt6r60fCz26Nd0Zqe0nbk1ZTIQbl3Kv7kYsX+yKMUFHzjaH2+AnM6vp2Xs+gNmaBAVWJjSmuPw76Efg==" crossorigin="anonymous" referrerpolicy="no-referrer" onload="renderMathInElement(document.body);"></script>

                <script>
                    document.addEventListener("DOMContentLoaded", function() {{
                        renderMathInElement(document.body, {{
                            delimiters: [
                                {{left: '$$', right: '$$', display: true}},
                                {{left: '$', right: '$', display: false}},
                                {{left: '\\\\(', right: '\\\\)', display: false}},
                                {{left: '\\\\[', right: '\\\\]', display: true}}
                            ],
                            throwOnError: false
                        }});
                    }});
                </script>

                <!-- Title -->
                <title>Chloe — {self.blog_post_data["post_title"]}</title>

                <!-- Favicon -->
                <link rel="icon" href="../../../assets/images/FAVICON.ico">
            </head>

            <body>
                <div class="wrapper">
                    <nav class="container">
                        <a class="nav-link" href="../../index.html"><div class="fa fa-house"></div></a>
                        <a class="nav-link" href="../../portfolio/portfolio.html"><div class="fa fa-briefcase"></div></a>
                        <a class="nav-link" href="../blog.html"><div class="fa fa-newspaper"></div></a>
                        <a class="nav-link" href="https://github.com/chloe-dev/" target="_blank"><div class="fab fa-github"></div></a>
                        <a class="nav-link" href="https://x.com/0x43484C4F45" target="_blank"><div class="fab fa-x-twitter"></div></a>
                    </nav>

                    <div class="container">
                        <h1>{self.blog_post_data["post_title"]}</h1>
                        <hr>
                        <p>{self.blog_post_data["publication_date"]}</p>
                        <hr>
                        {self.blog_post_data["post_content"]}
                    </div>

                    <footer class="container">
                        <p><a href="https://github.com/JetBrains/JetBrainsMono" target="_blank">JetBrains Mono</a> typeface by JetBrains, <a href="https://github.com/JulietaUla/Montserrat" target="_blank">Montserrat</a> by Julieta Ulanovsky et al.</p>
                        <br>
                        <p>Copyright &copy; 2025, <a href="mailto:contact@chloe.bio">Chloe B</a>. All Rights Reserved.</p>
                    </footer>
                </div>
            </body>
        </html>"""

        self.file_name: str = self.blog_post_data["post_id"] + "_" + self.blog_post_data["post_title"] + ".html"

        self.file_name = self.file_name.replace(" ", "_")

        try:
            with open(self.file_name, "x", encoding="utf-8") as html_file:
                html_file.write(html_document)
        except FileExistsError: # If the file already exists.
            print("[-]: A blog post with the same ID and title already exists.")
            return False
        except PermissionError: # If lacking permission to open/write to the file.
            print(f"[-]: Permission to open or write to {self.file_name} was denied.")
            return False
        except OSError: # If a general operating system related error occurs.
            print(f"[-]: Generic OS error occurred whilst attempting to open and write to {self.file_name}.")
            return False

        return True


    def emplace_post_listing(self) -> bool:
        html_listing: str = f"""
	    <a class="blog-listing-wrapper" href="posts/{self.file_name}" target="_blank">
		    <div class="blog-listing">
		        <h1>{self.blog_post_data["post_title"]}</h1>
		        <hr>
		        <p>{self.blog_post_data["publication_date"]}</p>
		        <hr>
		        <p>{self.blog_post_data["post_description"]}</p>
		    </div>
	    </a>"""

        try:
            with open("../blog.html", "r+", encoding="utf-8") as html_file:
                html_file_contents: str = html_file.read()

                insertion_point = html_file_contents.find("</nav>")

                if insertion_point == -1:
                    print("[-]: No valid insertion point was found.")
                    return False

                updated_html = (
                        html_file_contents[:insertion_point + 6] + 
                        '\n' + 
                        html_listing + 
                        html_file_contents[insertion_point + 6:]
                )

                html_file.seek(0)
                html_file.write(updated_html)
                html_file.truncate()
        except FileNotFoundError: # If blog.html is not found.
            print("[-]: blog.html could not be located.")
            return False
        except PermissionError: # If lacking permission to open/read/write to the file.
            print("[-]: Permission to open, read, or write to blog.html was denied.")
            return False
        except OSError: # If a general operating system related error occurs.
            print("[-]: Generic OS error occurred whilst attempting to open, read, or write to blog.html.")
            return False

        return True


def get_arguments() -> Namespace:
    argument_parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Convert Markdown to HTML for blogging.")

    argument_parser.add_argument("markdown_file_path", type=Path, help="Path to the Markdown file to be converted.")

    return argument_parser.parse_args()


def main() -> None:
    arguments: Namespace = get_arguments()

    blog_post_generator: Generator = Generator(arguments.markdown_file_path)

    if (
        blog_post_generator.set_blog_post_data() and
        blog_post_generator.generate_blog_post() and
        blog_post_generator.emplace_post_listing()
    ):
        print("[+]: The program has executed successfully; the blog post has been generated and its listing emplaced.")
    else:
        print("[-]: The program has executed unsuccessfully; see output above for more detailed information.")


if __name__ == "__main__":
    main()
