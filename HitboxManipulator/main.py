from application import App
from arcade.resources import add_resource_handle

if __name__ == '__main__':
    add_resource_handle("source", "resources")
    app = App()
    app.run()

