# 🍲 Local Food Wastage Management System

## 📌 Project Overview
Food wastage is a major issue worldwide — restaurants, grocery stores, and households throw away surplus food while many people face food insecurity.  
This project develops a **Local Food Wastage Management System** that connects **food providers** (restaurants, stores, individuals) with **receivers** (NGOs, individuals in need).  

The system allows:
- Providers to **list surplus food**  
- Receivers to **claim food**  
- SQL database to store and analyze data  
- A **Streamlit dashboard** to visualize insights & manage food listings  

---

## 🎯 Objectives
- Reduce food waste by redistributing surplus food  
- Provide real-time insights into donations & claims  
- Enable CRUD (Create, Read, Update, Delete) operations on food listings  
- Make the platform accessible with a web-based interface  

---

## 🗂️ Datasets
The system uses 4 datasets:  
1. **Providers Dataset (`providers_data.csv`)**  
   - Provider_ID, Name, Type, Address, City, Contact  

2. **Receivers Dataset (`receivers_data.csv`)**  
   - Receiver_ID, Name, Type, City, Contact  

3. **Food Listings Dataset (`food_listings_data.csv`)**  
   - Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type, (Latitude, Longitude optional)  

4. **Claims Dataset (`claims_data.csv`)**  
   - Claim_ID, Food_ID, Receiver_ID, Status, Timestamp  

---

## 🛠️ Tech Stack
- **Python**  
- **Streamlit** → Interactive dashboard  
- **SQL (SQLite)** → Database & queries  
- **Pandas** → Data analysis  
- **Plotly** → Charts & visualizations  
- **Geopy** → (Optional) geocoding city → coordinates for maps  

---

## ⚙️ Features
✅ Upload & clean datasets into SQL database  
✅ 15 SQL queries with interactive **Plotly visualizations**  
✅ Full **CRUD operations** (Create, Read, Update, Delete)  
✅ Dashboard-style navigation with **Streamlit sidebar**  
✅ Filtering by **city, provider, food type, meal type**  
✅ Claim status distribution analysis  
✅ (Optional) Interactive map of food listings  

---

## 📊 SQL Queries Implemented
The system answers 15 key questions:

1. Number of providers per city  
2. Number of receivers per city  
3. Provider type contributing most food  
4. Provider contact info in a specific city  
5. Receivers with most claims  
6. Total food quantity available  
7. City with most food listings  
8. Most common food types  
9. Claims per food item  
10. Provider with most successful claims  
11. Distribution of claim status (Completed / Pending / Cancelled)  
12. Average quantity of food claimed per receiver  
13. Most claimed meal type  
14. Total food donated by each provider  
15. Food quantity per city  

---

## 📷 Dashboard Preview
The dashboard has 4 sections (via sidebar navigation):  
- 🏠 **Overview** → Quick stats & claim status summary  
- 🍴 **Food Listings** → Browse/filter food by city/type/meal  
- 📈 **Analysis** → SQL insights with interactive charts  
- 🛠 **CRUD Operations** → Add, update, delete food listings  

---

## 🚀 How to Run Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/FoodWasteProject.git
   cd FoodWasteProject
   ```
2.Install dependencies:
```bash
pip install -r requirements.txt
```
3.Build the database:
```bash
python setup_database.py
```
4.Run the Streamlit app:
```bash
streamlit run app.py
```
### 🌐 Deployment (Streamlit Cloud)

-This project can be deployed for free using Streamlit Cloud:

-Push the project to GitHub

-Go to Streamlit Cloud → Log in with GitHub

-Click New App → Select repo → Choose app.py as entry point

-Add dependencies in requirements.txt (already included)

-Deploy 🚀 → Share the public URL

## App Link :
```
https://foodwasteproject-vhkfho6tlgk8lhtwxvx9hw.streamlit.app/
```
### 📈 Results

-Fully functional Streamlit dashboard

-SQL-powered insights on food donations & claims

-CRUD functionality for food listings

-Visualizations for all 15 queries

-Can be shared online for real-time access

### 👨‍💻 Skills Gained

-Python scripting

-SQL database creation & queries

-Data visualization with Plotly

-Building dashboards with Streamlit

-CRUD operations integration

-Deploying projects on Streamlit Cloud

### 📜 License

This project is for educational purposes as part of a capstone project on Food Wastage Management.
