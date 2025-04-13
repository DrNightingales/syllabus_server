'''
Application entry point
'''
from syllabus_app import create_app
app = create_app()
print(app.template_folder)
if __name__ == '__main__':
    app.run()
