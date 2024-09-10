
Setting Up the Development Environment

1. Clone the repository.

Setting Up A Virtual Environment

To ensure the project dependencies are properly managed and isolated, follow these steps to set up a virtual environment for the project.

2. Create the Virtual Environment

In the root of your project directory, run the following command in a bash terminal to create a virtual environment:

python -m venv venv

3. Activate the Virtual Environment

For Windows:
Run the following command in your terminal

source venv/Scripts/activate

For macOS/Linux:
Run the following command in your terminal:

source venv/bin/activate

Once activated, you should see (venv) in front of your terminal prompt, indicating that the virtual environment is active.

4. Install Dependencies

After activating the virtual environment, install the required dependencies by running:

pip install -r requirements.txt

5. Deactivating the Virtual Environment
When you're done, you can deactivate the virtual environment by running:

deactivate