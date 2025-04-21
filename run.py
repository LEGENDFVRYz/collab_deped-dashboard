from src.app import app
import time

# Compile all the scss to css:
# sass.compile(dirname=("src/assets/scss", "src/assets/css"))


# Run the dashboard project:
if __name__ == '__main__':
    # Temporary run file loop for development process
    # while True:
    #     try:
            app.run(debug=True)
        # except Exception as e:
        #     print(f"Failed due to {e}: restarting...")
        #     time.sleep(1)
        