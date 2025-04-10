# **SheetFlow Backend**  
A FastAPI backend for managing spreadsheet templates, sheets, and data with Excel export functionality.

## **Project Overview**  
SheetFlow is a powerful spreadsheet management system that allows users to:
- Create and manage templates with multiple sheets
- Define columns with different data types and requirements
- Add, update, and delete rows of data
- Export data to Excel files with proper formatting

## **Cloning the Repository**  

1. **Fork the repository** and clone it:  
   ```sh
   git clone https://github.com/<username>/sheetflow-backend.git
   ```
2. **Navigate into the project directory**:  
   ```sh
   cd sheetflow-backend
   ```

## **Setup Instructions**  

1. **Create a virtual environment**:  
   ```sh
   python3 -m venv venv
   ```
2. **Activate the virtual environment**:  
   - On macOS/Linux:  
     ```sh
     source venv/bin/activate
     ```
   - On Windows (PowerShell):  
     ```sh
     venv\Scripts\Activate
     ```
3. **Install project dependencies**:  
   ```sh
   pip install -r requirements.txt
   ```
4. **Create a `.env` file** from `.env.sample`:  
   ```sh
   cp .env.sample .env
   ```
5. **Start the server**:  
   ```sh
   python main.py
   ```

---

## **Database Setup**  

### **Replacing Placeholders in Database Setup**  

When setting up the database, you need to replace **placeholders** with your actual values. Below is a breakdown of where to replace them:

---

## **Step 1: Create a Database User**
```sql
CREATE USER user WITH PASSWORD 'your_password';
```
🔹 **Replace:**  
- `user` → Your **preferred database username** (e.g., `sheetflow_user`).  
- `'your_password'` → A **secure password** for the user (e.g., `'StrongP@ssw0rd'`).  

✅ **Example:**  
```sql
CREATE USER sheetflow_user WITH PASSWORD 'StrongP@ssw0rd';
```

---

## **Step 2: Create the Database**
```sql
CREATE DATABASE sheetflow_db;
```
🔹 **Replace:**  
- `sheetflow_db` → Your **preferred database name**.  

✅ **Example:**  
```sql
CREATE DATABASE sheetflow_db;
```

---

## **Step 3: Grant Permissions**
```sql
GRANT ALL PRIVILEGES ON DATABASE sheetflow_db TO user;
```
🔹 **Replace:**  
- `sheetflow_db` → The **database name you used** in Step 2.  
- `user` → The **username you created** in Step 1.  

✅ **Example:**  
```sql
GRANT ALL PRIVILEGES ON DATABASE sheetflow_db TO sheetflow_user;
```

---

## **Step 4: Update `.env` File**
Edit the `.env` file to match your setup.

```env
DATABASE_URL=postgresql://user:your_password@localhost/sheetflow_db
```
🔹 **Replace:**  
- `user` → Your **database username**.  
- `your_password` → Your **database password**.  
- `sheetflow_db` → Your **database name**.  

✅ **Example:**  
```env
DATABASE_URL=postgresql://sheetflow_user:StrongP@ssw0rd@localhost/sheetflow_db
```

---

## **Step 5: Verify Connection**
After setting up the database, test the connection:

```sh
psql -U user -d sheetflow_db -h localhost
```
🔹 **Replace:**  
- `user` → Your **database username**.  
- `sheetflow_db` → Your **database name**.  

✅ **Example:**  
```sh
psql -U sheetflow_user -d sheetflow_db -h localhost
```

## **Step 6: Run database migrations**  
   ```sh
   alembic upgrade head
   ```
   _Do NOT run `alembic revision --autogenerate -m 'initial migration'` initially!_

## **Step 7: If making changes to database models, update migrations**  
```sh
   alembic revision --autogenerate -m 'your migration message'
   alembic upgrade head
   ```

---

## **API Endpoints**  

### **Templates**
- `POST /api/v1/templates/create` - Create a new template
- `GET /api/v1/templates/{template_id}` - Get a template by ID
- `GET /api/v1/templates` - Get all templates
- `DELETE /api/v1/templates/{template_id}` - Delete a template

### **Rows**
- `POST /api/v1/rows/create` - Create a new row
- `POST /api/v1/rows/batch` - Create multiple rows in a batch
- `PUT /api/v1/rows/{row_id}` - Update a row
- `DELETE /api/v1/rows/{row_id}` - Delete a row
- `GET /api/v1/rows/sheet/{template_id}/{sheet_no}` - Get all rows for a sheet
- `GET /api/v1/rows/excel_download/{template_id}` - Download data as Excel file

### **Authentication**
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login a user

---

## **Excel Export Functionality**  

SheetFlow provides functionality to export data to Excel files with proper formatting:

- Headers are formatted with bold text, text wrapping, and a gray background
- Column widths are set for better readability
- Data is organized by sheets as defined in the template

The Excel export endpoint (`GET /api/v1/rows/excel_download/{template_id}`) generates a temporary Excel file that is automatically cleaned up after the response is sent to the client.

---

## **Adding New Routes**  

1. **Check if a related route file already exists** in `api/v1/routes/`.  
   - If yes, add your route inside the existing file.  
   - If no, create a new file following the naming convention.  
2. **Define the router** inside the new route file:  
   - Include the prefix (without `/api/v1` since it's already handled).  
3. **Register the router in `api/v1/routes/__init__.py`**:  
   ```python
   from .new_route import router as new_router
   api_version_one.include_router(new_router)
   ```

---

## **Running Tests with Pytest**  

### **Install Pytest**  
Ensure `pytest` is installed in your virtual environment:  
```sh
pip install pytest
```

### **Run all tests in the project**  
From the **project root directory**, run:  
```sh
pytest
```
This will automatically discover and execute all test files in the `tests/` directory.

### **Run tests with detailed output**  
For verbose output, add the `-v` flag:  
```sh
pytest -v
```

### **Run tests and generate coverage report**  
To check test coverage, install `pytest-cov`:  
```sh
pip install pytest-cov
```
Then run:  
```sh
pytest --cov=api
```

---

## **Common Migration Issues & Solutions**  

### **Error: "Target database is not up to date."**  
If you encounter this issue when running:  
```sh
alembic revision --autogenerate -m 'your migration message'
```
#### **Solution**:  
Run the following command first:  
```sh
alembic upgrade head
```
Then retry:  
```sh
alembic revision --autogenerate -m 'your migration message'
```

---

## **Dependencies**  

The project relies on the following key dependencies:
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **Pandas** - Data manipulation
- **XlsxWriter** - Excel file generation
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

For a complete list of dependencies, see `requirements.txt`.

