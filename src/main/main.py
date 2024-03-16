from src.main.app.app import App

if __name__ == "__main__":
    app = App('../../database/graph_manager.db')
    # app.generate_graph_window.generate_button.invoke()
    app.mainloop()

