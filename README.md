# SPM_T4

Pre-requisites
1. Please have Node.js installed. I am using v20.17.0(LTS)
2. Please have Python 3 installed

Setup Instructions

1. Clone this repository
2. Go to terminal in your VSCode repo, `cd frontend` then `npm install` / `npm i` to install vue packages
3. `npm run dev` to get vue frontend server up and running. It should be on `http://localhost:5173/`
4. `npm i axios` to install Axios library if you haven't already
5. `cd backend` to go into backend folder, run `python3 -m venv venv` (MacOS) to setup Python virtual environment. Windows users can refer to this link, https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html 
This helps ensure this Flask project won't affect others on the same machine with different Flask versions.
6. Activate the virtual environment with `source venv/bin/activate` (MacOS) / `venv\Scripts\activate (Windows)`. Then run `pip install -r requirements.txt` or try `pip3 install -r requirements.txt`