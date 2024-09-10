
## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0** license.

- You may download and view the code for personal or non-commercial purposes.
- You may not modify, distribute, or use this work for commercial purposes without explicit permission from the author, 
**Henri F. Urushihara**.

[Full License Details](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode)


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