from flask import Flask, render_template, request
import wikipediaapi
import mwparserfromhell
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company = request.form.get('company')
        filename = request.form.get('filename')

        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(company)

        if page_py.exists():
            text = page_py.summary[0:600]

            wikicode = mwparserfromhell.parse(page_py.text)
            templates = wikicode.filter_templates()

            founded = ''
            founders = ''
            headquarters = ''

            for template in templates:
                if template.name.strip().lower() == 'infobox company':
                    for param in template.params:
                        if 'founded' in param.name.strip().lower():
                            founded = param.value.strip()
                        if 'founders' in param.name.strip().lower():
                            founders = param.value.strip()
                        if 'hqs' in param.name.strip().lower():
                            headquarters = param.value.strip()

            # Save .md file in specified path
            file_path = os.path.join('G:\\', 'Other computers', 'My Computer', 'GigaVault',
                                     'Businesses & Organizations', filename + '.md')

            with open(file_path, 'w') as file:
                file.write(
                    "---\n"
                    "banner: \"![[B & O banner.jpg]]\"\n"
                    "banner_y: 0.308\n"
                    "---\n\n"
                    "# {}\n\n"
                    "## Founded by: {}\n\n"
                    "## Founded on: {}\n\n"
                    "## Headquarters: {}\n\n"
                    "## Summary:\n"
                    "{}\n\n"
                    "## Offerings, Assets, Services\n"
                    "- \n".format(company, founders, founded, headquarters, text)
                )

        return render_template('index.html', company=company, filename=filename)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8585)
