🚀 **Employee Management System**

A full-stack, production-ready Employee Management System built using modern technologies with complete infrastructure automation using Terraform and deployed on AWS.

🧩 **Project Overview**

This application enables administrators to manage employees with full CRUD operations, along with secure authentication and role-based access control (RBAC).

The system is designed to be:

      🔐 Secure (JWT + password hashing)
      ⚡ Scalable (serverless backend + CDN)
      ☁️ Cloud-native (AWS)
      🧱 Fully automated (Terraform)
      🛠️ Backend (FastAPI)
      
            **Technologies**
                  Python
                  FastAPI
                  MongoDB
                  REST APIs
                  
            **Features**
                🔐 Authentication & Security
                      User registration & login
                      Password hashing using bcrypt
                      JWT-based authentication
                      Token validation middleware
                      Secure protected routes  
                
            🧑‍💼** Role-Based Access Control (RBAC)**
                      Role	        Permissions
                      Admin	        Full CRUD
                      Manager	        Read + limited update
                      Employee	  Read-only (self data)
                
            📌 **CRUD APIs**
                      Method	Endpoint
                      POST	/employees
                      GET	/employees
                      GET	/employees/{id}
                      PUT	/employees/{id}
                      DELETE	/employees/{id}
                
            🗄️ **Database**
                MongoDB hosted on EC2
                **Collections:**
                  users
                  employees
                  
            📁 **Backend Structure**
                  app/
                   ├── main.py
                   ├── routes/
                   ├── models/
                   ├── schemas/
                   ├── services/
                   ├── auth/
                   └── database/
            
             
            🎨 **Frontend (React)**
                  Technologies
                  React
                  HTML
                  CSS
                  Axios
                  
            **Features**
                🔐 Authentication UI
                Login page
                Registration page
                JWT stored in localStorage
                📊 Employee Management
                Dashboard
                Employee list
                Add/Edit/Delete employee
                🔀 Routing
                React Router
                Protected routes (JWT-based)
                ⚙️ State Management
                useState
                useEffect
                Axios for API calls
                
            📁 **Frontend Structure**
                frontend/
                 ├── components/
                 │    ├── Login.js
                 │    ├── Register.js
                 │    ├── Dashboard.js
                 │    ├── EmployeeList.js
                 │    └── EmployeeForm.js
                 └── App.js
                 
            ☁️** AWS Infrastructure (Provisioned with Terraform)**
            
            **All infrastructure is fully automated using Terraform (no manual setup).**
            
            **Services Used**
                Service	          Purpose
                S3	              Host React frontend
                CloudFront	      CDN distribution
                API Gateway	      Expose backend APIs
                Lambda	          Run FastAPI backend
                EC2	              Host MongoDB
                IAM              	Roles & permissions
                
            🔧** Infrastructure Details**
                📦 S3
                Static website hosting enabled
                Stores React build files
                🌍 CloudFront
                CDN for frontend
                HTTPS enabled
                Origin Access Control (OAC)
                🔌 API Gateway
                Connects to Lambda
                Handles routing & CORS
                ⚡ Lambda
                Runs FastAPI using Mangum
                Handles backend APIs
                🖥️ EC2
                Hosts MongoDB
                Configured with secure access
                Uses user_data for setup
                
            🧱** Terraform Setup**
              📁 **Structure**
                terraform/
                 ├── main.tf
                 ├── variables.tf
                 ├── outputs.tf
                 ├── provider.tf
                 └── terraform.tfvars
                 
            ⚙️** Terraform Features**
                Uses variables for flexibility
                Outputs important resource values (URLs, IDs)
                Modular design (optional modules for scalability)
                
            **Fully provisions:**
                S3 bucket
                CloudFront distribution
                Lambda function
                API Gateway
                EC2 instance
                Security groups
                IAM roles
                
            ▶️** Terraform Commands**
                  terraform init
                  terraform plan
                  terraform apply
                  
            
            **  CI/CD (Optional)**     
            **GitHub Actions Pipeline**
            Build React app → deploy to S3
            Package backend → deploy to Lambda
            Run Terraform apply
            
            📦 Deployment Steps
            Clone repository
            Configure environment variables
            
            Build frontend:
            
            npm run build
            Package backend for Lambda
            
            Run Terraform:
            
            terraform init
            terraform apply
            Access application via CloudFront URL
            
            🔑 Environment Variables
            Backend (.env)
            MONGO_URI=
            JWT_SECRET=
            ALGORITHM=HS256
            ACCESS_TOKEN_EXPIRE_MINUTES=60
            
            🧪 API Testing
            Example (cURL)
            curl -X POST http://<api-url>/login \
            -H "Content-Type: application/json" \
            -d '{"email":"admin@test.com","password":"123456"}'
            
            🎯 **Project Goals**
            ✅ Fully automated infrastructure (Terraform)
            🔐 Secure authentication (JWT + hashing)
            🧑‍💼 RBAC implementation
            ☁️ Cloud deployment on AWS
            ⚡ Scalable and production-ready architecture
            
            
            This project demonstrates:
            
            Full-stack development (React + FastAPI)
            Cloud deployment using AWS
            Infrastructure as Code (Terraform)
            Secure API design
