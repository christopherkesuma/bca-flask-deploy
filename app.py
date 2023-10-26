from config import connex_app

connex_app.add_api("swagger.yml")
# testing

if __name__ == "__main__":
    connex_app.run(debug=True)