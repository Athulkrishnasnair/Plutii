from app import create_app

# Boilerplate
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)