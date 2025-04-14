'''
Application entry point
'''
from syllabus_app import create_app
from syllabus_app.config import Config

app = create_app()
print("Template folder is:", app.template_folder)

if __name__ == '__main__':

    app.run(debug=Config.DEBUG)

