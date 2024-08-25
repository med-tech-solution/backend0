## How to run the Backend Server

### 1. Install the required packages
```bash
pip install -r requirements.txt
```

### 2. Set the environment variables
```bash
TOGETHER_API_KEY=
ADMIN_MAIL=
ORGANIZATION_ID=
CLIENT_ID=
CLIENT_SECRET=
CLIENT_PUBLIC_ID=
APP_ID=
APP_CLIENT=
APP_CONFIDENTIAL_CLIENT=
APP_SECRET=
TENANCY=
```

### 3. Run the application
```bash
cd flask_server
python3 app.py
```

### 4. Required Operating System
- Linux based
- MacOS

### Directory structure
```
.
├── README.md
├── flask_server
│   ├── app.py (entry point)
│   ├── arg_generator_cllama_utils.py (utility functions for generating arguments)
│   ├── code_ast.py (AST generation)
│   ├── code_llama_utils.py (utility functions for code llama)
│   ├── common_imports.py (common imports those are used in all the files)
│   ├── log_emb.py (For inserting logs in entry and exit of functions)
│   ├── opentext_utils.py (utility functions for opentext, email, services)
│   ├── opt_utils.py (utility functions for optimization using code llama)
│   ├── profile_anal.py (profile analysis)
│   ├── profile_utils.py (async functions for profile analysis)
│   ├── utils.py (utility functions)
├── function_logs (For storing logs of functions entry and exit)
├── profile_logs (For storing logs of profile analysis)
├── interim_projects (For storing intermediate projects)
├── target_projects (For storing target projects, extracted from the zip file)
├── requirements.txt
├── .gitignore
├── .env (For storing environment variables)
```

### Formula analysis
- The formula analysis utility stored in `flask_server/profile_anal.py` file.