create a virtual environment and install the necessary dependencies for your Flask app:

1. First, make sure you have `virtualenv` installed. If not, you can install it using `pip`:
```python
pip install virtualenv
```

2. Next, navigate to the directory where you want to create your virtual environment and run the following command to create a new virtual environment:
```python
virtualenv venv
```

3. Activate the virtual environment by running the following command:
    - On Windows:
    ```python
    venv\Scripts\activate
    ```
    - On macOS or Linux:
    ```python
    source venv/bin/activate
    ```

4. Once the virtual environment is activated, you can install the necessary dependencies for your Flask app using `pip`:
```python
pip install flask flask-login flask-swagger
```

Now you can run your Flask app within the virtual environment, and all the dependencies will be installed in the virtual environment, isolated from your system-wide Python installation.