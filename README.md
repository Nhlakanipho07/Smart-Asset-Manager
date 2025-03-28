# How to setup the project:

### 1. Start by cloning this repo:

- Run ```git clone git@github.com:Nhlakanipho07/Smart-Asset-Manager.git``` in a linux terminal (gitbash for Windows os)

### 2. Navigate to the project directory:

- On a local computer, using a code editor, navigate to the cloned repository and open it in the code editor. This repository name will look as follows:
    - `Smart-Asset-Manager`

### 3. Set up a virtual environment:

- Open a terminal in the code editor, ensure that the terminal's working directory is this repo.

- In the terminal:
    - Create a virtual environment by running:
        - On Windows: `python -m venv <env>`
        - On Linux: `python3 -m venv <env>`

    - Activate the virtual environment:
        - On Windows, run  `<env>\Scripts\activate` 
        - On Linux, run `source <env>/bin/activate`

### 4. Install smart_asset_manager:

- In the terminal:
    - Run `pip install .`
    - Run `pip install -r requirements.txt`
    - To verify that `smart_asset_manager` and all dependancies are install successfully, run: `pip freeze`

# How to run smart_asset_manager:

- In the terminal:
    - On Windows, run `python run.py`
    - On Linux, run `python3 run.py`

# How to access endpoints:

1. Run `smart_asset_manager`

2. Install and setup `Postman` if not already installed.

3. Open `Postman` and select `Collections` in the top left-hand corner.

4. Create a collection by pressing `New`, then `Collection`.

### 5. Inside `New Collection`:

- **To get computers**:
    1. Select `Add a request` (highlighted in blue) or hover over `New Collection` and press the three dots on the right-side then press `Add request`.
    2. Rename `New Request` to `get_computers`.
    3. Set the HTTP request method to `GET` in the drop down.
    4. Paste the following url in the url area: `http://127.0.0.1:5000/computers?page=1&per_page=10`
    5. Press `Save`, then press `Send`.

    **Example response**:

    ```
    {
    "computers": [],
    "current_page": 1,
    "pages": 0,
    "per_page": 10,
    "total": 0
    }
    ```

- **To add a computer**:
    1. Hover over `New Collection` and press the three dots on the right-side then press `Add request`.
    2. Rename `New Request` to `add_computer`.
    3. Set the HTTP request method to `POST` in the drop down.
    4. Paste the following url in the url area: `http://127.0.0.1:5000/computer`
    5. Press `Body` under the url, then `raw`, then `JSON` in the drop down.
    6. In the text area paste a `JSON` object that contains the computer's details one wants to add to the database.
    5. Press `Save`, then press `Send`.
    
    **Example of computer details as a `JSON` object**:

    ```
    {
    "hard_drive_type": "SSD",
    "processor": "Intel Core i7",
    "ram_amount": 16,
    "maximum_ram": 32,
    "hard_drive_space": 512,
    "form_factor": "Laptop"
    }
    ```

    **Expected response**:

    ```
    {
    "message": "Computer added successfully"
    }
    ```

- **To edit a computer**:

    Assuming one has added the computer in the example above; after sending a `GET` request using `get_computer`, one should see a response as follows:

    ```
    {
        "computers": [
            {
                "form_factor": "Laptop",
                "hard_drive_space": 512,
                 "hard_drive_type": "SSD",
                "id": 1,
                "maximum_ram": 32,
                "processor": "Intel Core i7",
                "ram_amount": 16
            }
        ],
            
        "current_page": 1,
        "pages": 1,
        "per_page": 10,
        "total": 1
    }
    ```

    1. Hover over `New Collection` and press the three dots on the right-side then press `Add request`.
    2. Rename `New Request` to `edit_computer`.
    3. Set the HTTP request method to `PUT` in the drop down.
    4. Paste the following url in the url area: `http://127.0.0.1:5000/computer/<int:computer_id>`.
    5. To edit the details of the first computer in the database, replace `<int:computer_id>` with `1` in the url above.
    6. Press `Body` under the url, then `raw`, then `JSON` in the drop down.
    7. In the text area paste a `JSON` object that contains the updated computer's details.
    8. Press `Save`, then press `Send`.

    **Example computer details update**:

    ```
    {
    "form_factor": "Laptop",
    "hard_drive_space": 512,
    "hard_drive_type": "HDD",
    "id": 1,
    "maximum_ram": 32,
    "processor": "Intel Core i7",
    "ram_amount": 12
    }
    ```

    **Expected response**:

    ```
    {
    "message": "Computer updated successfully"
    }
    ```

    To see the update, send a `GET` request using `get_computers`:

    ```
    {
    "computers": [

        {
            "form_factor": "Laptop",
            "hard_drive_space": 512,
            "hard_drive_type": "HDD",
            "id": 1,
            "maximum_ram": 32,
            "processor": "Intel Core i7",
            "ram_amount": 12
        }
            
    ],
    "current_page": 1,
    "pages": 1,
    "per_page": 10,
    "total": 1
    }
    ```
- **To delete a computer**:
    1. Hover over `New Collection` and press the three dots on the right-side then press `Add request`.
    2. Rename `New Request` to `delete_computer`.
    3. Set the HTTP request method to `DELETE` in the drop down.
    4. Paste the following url in the url area: `http://127.0.0.1:5000/computer/<int:computer_id>`
    5. To delete the first computer in the database, replace `<int:computer_id>` with `1` in the url above.
    6. Press `Save`, then press `Send`.

    **Expected response**:
    ```
    {
    "message": "Computer deleted successfully"
    }
    ```

    To see that the first computer details are deleted, send a `GET` request using `get_computers`:
    ```
    {
    "computers": [],
    "current_page": 1,
    "pages": 0,
    "per_page": 10,
    "total": 0
    }
    ```

# How to run tests:

- In the terminal:
    - To run all tests:
        - On Windows: `python -m unittest tests/test_app.py`
        - On Linux: `python3 -m unittest tests/test_app.py`
    
    - To run a specific test:
        - On Windows: `python -m unittest tests.test_app.AppTestCase.<test_method_name>`
        - On linux: `python3 -m unittest tests.test_app.AppTestCase.<test_method_name>`
    
    *Note: replace `<test_method_name>` with a test method name of the specific test method found in `test_app.py`*

# How to deactivate virtual environment:

- Run `deactivate` in the terminal.

