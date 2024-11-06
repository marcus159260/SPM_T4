# SPM_T4

## Pre-requisites

1. Hve Node.js installed. I am using v20.17.0(LTS)
2. Have Python 3 installed

## Setup Instructions

1. Clone this repository
2. Go to terminal in the VSCode repo, `cd frontend` then `npm install` / `npm i` to install vue packages. Select 'No' for everything EXCEPT Vue Router ('Yes'). 
If you did not manage to select 'Yes' to install Vue Router, install with the command `npm install vue-router@4` in terminal instead.
3. `npm run dev` to get vue frontend server up. It should be running on `http://localhost:5173/`
4. Open new terminal, `cd frontend`, `npm i axios` to install Axios library if you haven't already
5. Open a new terminal, `cd backend` to go into backend folder, run `python3 -m venv venv` (MacOS, it should also work on Windows) to setup Python virtual environment. Windows users can refer to this link, https://python.land/virtual-environments/virtualenv
This helps ensure this Flask project won't affect others on the same machine with different Flask versions.
6. Activate the virtual environment with `source venv/bin/activate` (MacOS) / `venv\Scripts\activate.bat`(CMD on Windows). Then run `pip3 install -r requirements.txt` or try `pip install -r requirements.txt`. 
7. Run `python3 app.py` or `python app.py`. The Flask server should be live.
`deactivate` to deactivate virtual environment if you want to stop using it

## Unit Testing
1. For backend tests:
    - `cd backend/test/integration` for integration tests
    - `cd backend/test/unit` for unit tests
2. To run, type `pytest [filename].py`
3. To run all, type `pytest` either under integration or unit folder.
4. To run coverage for all tests, type `cd backend`
    - For integration tests: `pytest --cov=routes --cov=api --cov-report=html:test/integration/coverage_html test/integration/`
    - For unit tests: `pytest --cov=controllers --cov=api --cov report=html:test/unit/coverage_html test/unit/`

5. To open up the coverage HTML report, be directly either under `backend/test/integration` or `backend/test/integration` and type `start index.html`