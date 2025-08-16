import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from datetime import date

# -------------------------------------------------
# App config
# -------------------------------------------------
st.set_page_config(page_title="Food Waste Management", layout="wide")
engine = create_engine("sqlite:///food_waste.db")

# Small helpers
def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})

def execute(sql: str, params: dict | None = None) -> None:
    with engine.begin() as conn:
        conn.execute(text(sql), params or {})

# -------------------------------------------------
# Sidebar navigation
# -------------------------------------------------
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Overview", "🍴 Food Listings", "📈 Analysis (15 Queries)", "🛠 CRUD Operations"]
)

# -------------------------------------------------
# 1) OVERVIEW
# -------------------------------------------------
if page == "🏠 Overview":
    st.title("🍲 Local Food Wastage Management ")

    providers = run_query("SELECT * FROM providers")
    receivers = run_query("SELECT * FROM receivers")
    food = run_query("SELECT * FROM food_listings")
    claims = run_query("SELECT * FROM claims")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Providers", len(providers))
    col2.metric("Total Receivers", len(receivers))
    col3.metric("Food Listings", len(food))
    col4.metric("Total Claims", len(claims))

    # Claim status pie (Query 11)
    st.subheader("Claim Status Overview (Query 11)")
    q11 = "SELECT Status, COUNT(*) AS Count FROM claims GROUP BY Status"
    status_df = run_query(q11)
    if not status_df.empty:
        fig = px.pie(status_df, names="Status", values="Count", title="Claims Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No claims yet.")

    # Quantity by city (Query 15)
    st.subheader("Food Quantity by City (Query 15)")
    q15 = "SELECT Location, SUM(Quantity) AS Total_Quantity FROM food_listings GROUP BY Location"
    qty_city = run_query(q15)
    if not qty_city.empty:
        fig = px.bar(qty_city, x="Location", y="Total_Quantity", title="Total Quantity per City")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 2) FOOD LISTINGS
# -------------------------------------------------
elif page == "🍴 Food Listings":
    st.title("🍴 Food Listings")

    food = run_query("SELECT * FROM food_listings")
    if food.empty:
        st.warning("No food listings in the database yet.")
    else:
        # Filters
        c1, c2, c3 = st.columns(3)
        with c1:
            city = st.selectbox("Filter by City", options=["(All)"] + sorted(food["Location"].dropna().unique().tolist()))
        with c2:
            ftype = st.selectbox("Filter by Food Type", options=["(All)"] + sorted(food["Food_Type"].dropna().unique().tolist()))
        with c3:
            mtype = st.selectbox("Filter by Meal Type", options=["(All)"] + sorted(food["Meal_Type"].dropna().unique().tolist()))

        df = food.copy()
        if city != "(All)":
            df = df[df["Location"] == city]
        if ftype != "(All)":
            df = df[df["Food_Type"] == ftype]
        if mtype != "(All)":
            df = df[df["Meal_Type"] == mtype]

        st.dataframe(df, use_container_width=True)

        st.markdown("**Map** (requires `Latitude` and `Longitude` columns)")
        if {"Latitude", "Longitude"}.issubset(df.columns):
            st.map(df[["Latitude", "Longitude"]])
        else:
            st.info("Add `Latitude` and `Longitude` columns to `food_listings_data.csv` if you want the map to work.")

# -------------------------------------------------
# 3) ANALYSIS (All 15 queries visualized)
# -------------------------------------------------
elif page == "📈 Analysis (15 Queries)":
    st.title("📈 Analysis & SQL Insights (15 Queries)")

    # 1 Providers per City
    st.subheader("1) Providers per City")
    q1 = "SELECT City, COUNT(*) AS Provider_Count FROM providers GROUP BY City"
    df1 = run_query(q1)
    st.dataframe(df1, use_container_width=True)
    if not df1.empty:
        st.plotly_chart(px.bar(df1, x="City", y="Provider_Count", title="Providers per City"), use_container_width=True)

    # 2 Receivers per City
    st.subheader("2) Receivers per City")
    q2 = "SELECT City, COUNT(*) AS Receiver_Count FROM receivers GROUP BY City"
    df2 = run_query(q2)
    st.dataframe(df2, use_container_width=True)
    if not df2.empty:
        st.plotly_chart(px.bar(df2, x="City", y="Receiver_Count", title="Receivers per City"), use_container_width=True)

    # 3 Provider Type Contributions
    st.subheader("3) Provider Type Contributions")
    q3 = "SELECT Provider_Type, COUNT(*) AS Food_Count FROM food_listings GROUP BY Provider_Type ORDER BY Food_Count DESC"
    df3 = run_query(q3)
    st.dataframe(df3, use_container_width=True)
    if not df3.empty:
        st.plotly_chart(px.bar(df3, x="Provider_Type", y="Food_Count", title="Food Contributions by Provider Type"), use_container_width=True)

    # 4 Provider Contact Info by City (table only; add placeholder)
    st.subheader("4) Provider Contact Info by City")
    city_input = st.text_input("Enter City Name (e.g., Hyderabad, Chennai, Delhi)", placeholder="e.g., Hyderabad")
    if city_input.strip():
        q4 = "SELECT Name, Contact FROM providers WHERE City = :city"
        df4 = run_query(q4, {"city": city_input.strip()})
        st.dataframe(df4, use_container_width=True)
    else:
        st.info("Type a city to view provider contact info.")

    # 5 Receivers with most claims
    st.subheader("5) Top Receivers by Claims")
    q5 = """
        SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims
        FROM claims c JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Name ORDER BY Total_Claims DESC
    """
    df5 = run_query(q5)
    st.dataframe(df5, use_container_width=True)
    if not df5.empty:
        st.plotly_chart(px.bar(df5, x="Name", y="Total_Claims", title="Receivers with Most Claims"), use_container_width=True)

    # 6 Total quantity of food available (metric)
    st.subheader("6) Total Quantity of Food Available")
    q6 = "SELECT SUM(Quantity) AS Total_Quantity FROM food_listings"
    df6 = run_query(q6)
    total_qty = int(df6.iloc[0, 0]) if not df6.empty and pd.notna(df6.iloc[0, 0]) else 0
    st.metric("Total Quantity Available", total_qty)

    # 7 City with most food listings
    st.subheader("7) City with Most Food Listings")
    q7 = "SELECT Location, COUNT(*) AS Listings FROM food_listings GROUP BY Location ORDER BY Listings DESC"
    df7 = run_query(q7)
    st.dataframe(df7, use_container_width=True)
    if not df7.empty:
        st.plotly_chart(px.bar(df7, x="Location", y="Listings", title="Food Listings per City"), use_container_width=True)

    # 8 Most common food types
    st.subheader("8) Most Common Food Types")
    q8 = "SELECT Food_Type, COUNT(*) AS Count FROM food_listings GROUP BY Food_Type ORDER BY Count DESC"
    df8 = run_query(q8)
    st.dataframe(df8, use_container_width=True)
    if not df8.empty:
        st.plotly_chart(px.pie(df8, names="Food_Type", values="Count", title="Food Type Distribution"), use_container_width=True)

    # 9 Claims per food item
    st.subheader("9) Claims per Food Item")
    q9 = """
        SELECT f.Food_Name, COUNT(c.Claim_ID) AS Claims
        FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Food_Name
    """
    df9 = run_query(q9)
    st.dataframe(df9, use_container_width=True)
    if not df9.empty:
        st.plotly_chart(px.bar(df9, x="Food_Name", y="Claims", title="Claims per Food Item", orientation="v"), use_container_width=True)

    # 10 Provider with most successful claims
    st.subheader("10) Provider with Most Successful Claims")
    q10 = """
        SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Name ORDER BY Successful_Claims DESC
    """
    df10 = run_query(q10)
    st.dataframe(df10, use_container_width=True)
    if not df10.empty:
        st.plotly_chart(px.bar(df10, x="Name", y="Successful_Claims", title="Providers with Most Completed Claims"), use_container_width=True)

    # 11 Claim Status Distribution (already shown on Overview; kept here too)
    st.subheader("11) Claim Status Distribution")
    df11 = status_df if 'status_df' in locals() else run_query("SELECT Status, COUNT(*) AS Count FROM claims GROUP BY Status")
    st.dataframe(df11, use_container_width=True)
    if not df11.empty:
        st.plotly_chart(px.pie(df11, names="Status", values="Count", title="Claims Status"), use_container_width=True)

    # 12 Average quantity claimed per receiver
    st.subheader("12) Average Quantity Claimed per Receiver")
    q12 = """
        SELECT r.Name, AVG(f.Quantity) AS Avg_Quantity
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY r.Name
    """
    df12 = run_query(q12)
    st.dataframe(df12, use_container_width=True)
    if not df12.empty:
        st.plotly_chart(px.bar(df12, x="Name", y="Avg_Quantity", title="Avg Quantity Claimed per Receiver"), use_container_width=True)

    # 13 Most claimed meal type
    st.subheader("13) Most Claimed Meal Type")
    q13 = """
        SELECT Meal_Type, COUNT(*) AS Claims
        FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY Meal_Type ORDER BY Claims DESC
    """
    df13 = run_query(q13)
    st.dataframe(df13, use_container_width=True)
    if not df13.empty:
        st.plotly_chart(px.bar(df13, x="Meal_Type", y="Claims", title="Most Claimed Meal Types"), use_container_width=True)

    # 14 Total food donated by each provider
    st.subheader("14) Total Food Donated by Each Provider")
    q14 = """
        SELECT p.Name, SUM(f.Quantity) AS Total_Donated
        FROM food_listings f JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Name
    """
    df14 = run_query(q14)
    st.dataframe(df14, use_container_width=True)
    if not df14.empty:
        st.plotly_chart(px.bar(df14, x="Name", y="Total_Donated", title="Total Donated by Provider"), use_container_width=True)

    # 15 Food quantity per city (also on Overview)
    st.subheader("15) Food Quantity per City")
    df15 = qty_city if 'qty_city' in locals() else run_query("SELECT Location, SUM(Quantity) AS Total_Quantity FROM food_listings GROUP BY Location")
    st.dataframe(df15, use_container_width=True)
    if not df15.empty:
        st.plotly_chart(px.bar(df15, x="Location", y="Total_Quantity", title="Food Quantity per City"), use_container_width=True)

# -------------------------------------------------
# 4) CRUD OPERATIONS (Create, Read, Update, Delete)
# -------------------------------------------------
elif page == "🛠 CRUD Operations":
    st.title("🛠 Manage Food Listings")

    # CREATE
    st.subheader("➕ Add New Food Listing")
    with st.form("add_food"):
        c1, c2, c3 = st.columns(3)
        with c1:
            food_name = st.text_input("Food Name", placeholder="e.g., Rice, Pizza, Sandwich")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            expiry_date = st.date_input("Expiry Date", value=date.today())
        with c2:
            provider_id = st.number_input("Provider ID", min_value=1)
            provider_type = st.text_input("Provider Type", placeholder="e.g., Restaurant, Grocery Store, Supermarket")
            location = st.text_input("City", placeholder="e.g., Hyderabad, Chennai, Delhi")
        with c3:
            food_type = st.text_input("Food Type", placeholder="e.g., Veg, Non-Veg, Vegan")
            meal_type = st.text_input("Meal Type", placeholder="e.g., Breakfast, Lunch, Dinner, Snacks")

        submitted = st.form_submit_button("Add Food")
        if submitted:
            execute(
                """
                INSERT INTO food_listings
                (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                VALUES (:Food_Name, :Quantity, :Expiry_Date, :Provider_ID, :Provider_Type, :Location, :Food_Type, :Meal_Type)
                """,
                {
                    "Food_Name": food_name,
                    "Quantity": int(quantity),
                    "Expiry_Date": str(expiry_date),
                    "Provider_ID": int(provider_id),
                    "Provider_Type": provider_type,
                    "Location": location,
                    "Food_Type": food_type,
                    "Meal_Type": meal_type,
                }
            )
            st.success("✅ New food listing added.")

    st.markdown("---")

    # READ (quick view)
    st.subheader("📖 Current Food Listings")
    current_food = run_query("SELECT * FROM food_listings")
    st.dataframe(current_food, use_container_width=True)

    st.markdown("---")

    # UPDATE
    st.subheader("✏️ Update a Food Listing")
    if current_food.empty:
        st.info("No food to update.")
    else:
        to_update_id = st.selectbox("Select Food_ID to update", options=current_food["Food_ID"].tolist())
        row = current_food[current_food["Food_ID"] == to_update_id].iloc[0]

        with st.form("update_food"):
            c1, c2, c3 = st.columns(3)
            with c1:
                new_name = st.text_input("Food Name", value=str(row["Food_Name"]))
                new_qty = st.number_input("Quantity", min_value=1, value=int(row["Quantity"]))
                new_expiry = st.date_input("Expiry Date", value=pd.to_datetime(row["Expiry_Date"]).date() if pd.notna(row["Expiry_Date"]) else date.today())
            with c2:
                new_provider_id = st.number_input("Provider ID", min_value=1, value=int(row["Provider_ID"]))
                new_provider_type = st.text_input("Provider Type", value=str(row["Provider_Type"]))
                new_location = st.text_input("City", value=str(row["Location"]))
            with c3:
                new_food_type = st.text_input("Food Type", value=str(row["Food_Type"]))
                new_meal_type = st.text_input("Meal Type", value=str(row["Meal_Type"]))

            update_submit = st.form_submit_button("Update")
            if update_submit:
                execute(
                    """
                    UPDATE food_listings
                    SET Food_Name = :Food_Name,
                        Quantity = :Quantity,
                        Expiry_Date = :Expiry_Date,
                        Provider_ID = :Provider_ID,
                        Provider_Type = :Provider_Type,
                        Location = :Location,
                        Food_Type = :Food_Type,
                        Meal_Type = :Meal_Type
                    WHERE Food_ID = :Food_ID
                    """,
                    {
                        "Food_Name": new_name,
                        "Quantity": int(new_qty),
                        "Expiry_Date": str(new_expiry),
                        "Provider_ID": int(new_provider_id),
                        "Provider_Type": new_provider_type,
                        "Location": new_location,
                        "Food_Type": new_food_type,
                        "Meal_Type": new_meal_type,
                        "Food_ID": int(to_update_id),
                    }
                )
                st.success("✅ Food listing updated.")

    st.markdown("---")

    # DELETE (expired or specific)
    st.subheader("🗑️ Delete Expired Food")
    if st.button("Delete All Expired (Expiry_Date < today)"):
        execute("DELETE FROM food_listings WHERE date(Expiry_Date) < date('now')")
        st.success("✅ Expired food items removed.")

    st.subheader("🗑️ Delete by Food_ID")
    if current_food.empty:
        st.info("No food to delete.")
    else:
        del_id = st.selectbox("Choose Food_ID to delete", options=current_food["Food_ID"].tolist(), key="delete_id")
        if st.button("Delete Selected"):
            execute("DELETE FROM food_listings WHERE Food_ID = :fid", {"fid": int(del_id)})
            st.success(f"✅ Deleted Food_ID {del_id}.")
