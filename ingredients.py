from google import genai
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from flask import jsonify
import markdown

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/modify', methods=['POST'])
def modify():
    recipe_url = request.form["recipeUrl"]
    substitution = request.form["substitution"]
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(f"Please modify the recipe from this link: {recipe_url}. "
                 f"Apply this change: {substitution}")
    )
    nutrition_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(f"Can you display the nutrition information of: {response.text}")
    )
    styles = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(f"Can you generate ccs for {nutrition_response.text}, only the ccs nothing else no extra words")
    )

    css = styles.text
    modified_recipe = markdown.markdown(response.text)
    nutrition = markdown.markdown(nutrition_response.text)

    return render_template("editRecipe.html", modified_recipe=modified_recipe, nutrition=nutrition, css=css)



if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=8000)