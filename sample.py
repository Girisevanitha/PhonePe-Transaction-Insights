import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as db
import plotly.express as px
import pandas as pd
import requests
import json
from PIL import Image
import mysql.connector


host='localhost'
passcode='Evanitha0805@'
user='girisevanitha'
db_name='project_phonepe'

db_connection=db.connect(
    user=user,
    host=host,
    password=passcode,
    database=db_name
) 
curr=db_connection.cursor()



curr.execute("SELECT * FROM ag_insurance")
Data1=curr.fetchall()
aggre_ins=pd.DataFrame(Data1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

curr.execute("SELECT * FROM ag_transaction")
Data2=curr.fetchall()
aggre_trans=pd.DataFrame(Data2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

curr.execute("SELECT * FROM ag_user")
Data3=curr.fetchall()
aggre_users=pd.DataFrame(Data3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))

curr.execute("SELECT * FROM mp_insurance")
Data4=curr.fetchall()
map_ins=pd.DataFrame(Data4,columns=("States","Years","Quarter","District","Transaction_count","Transaction_amount"))

curr.execute("SELECT * FROM mp_trans")
Data5=curr.fetchall()
map_trans=pd.DataFrame(Data5,columns=("States","Years","Quarter","District","Transaction_count","Transaction_amount"))

curr.execute("SELECT * FROM mp_user")
Data6=curr.fetchall()
map_users=pd.DataFrame(Data6,columns=("States","Years","Quarter","District","Registeredusers","AppOpens"))

curr.execute("SELECT * FROM top_insurance")
Data7=curr.fetchall()
top_ins=pd.DataFrame(Data7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))


curr.execute("SELECT * FROM top_trans")
Data8=curr.fetchall()
top_trans=pd.DataFrame(Data8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

curr.execute("SELECT * FROM top_users")
Data9=curr.fetchall()
top_users=pd.DataFrame(Data9,columns=("States","Years","Quarter","Pincodes","Registeredusers"))


#Creating Streamlit 

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "BUSINESS CASE STUDY"])


if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\Prakash\Desktop\MDT48\phonepe\images.jpg"))

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\Prakash\Desktop\MDT48\phonepe\images (1).jpg"))

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\Prakash\Desktop\MDT48\phonepe\images (2).jpg"))
    
   

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="girisevanitha",
        password="Evanitha0805@",
        database="project_phonepe"
    )


def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    cols = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=cols)


if select == "BUSINESS CASE STUDY":

    st.title("📊 PhonePe Business Case Study Dashboard")

    
    st.sidebar.title("Select Business Case Study")
    case_study = st.sidebar.selectbox("Choose one:", [
        "1. Transaction Dynamics",
        "2. Device Usage",
        "3. Insurance Engagement",
        "4. User Registration Analysis",
        "5. Insurance Transactions Insights"
    ])

    # Visualizations of Business case study

    if case_study == "1. Transaction Dynamics":
      st.subheader("📈 Transaction Trends by State and Year")

      df = run_query("""
            SELECT states, years, quarter, SUM(transaction_count) AS total_txns
            FROM ag_transaction
            GROUP BY states, years, quarter
            ORDER BY years, quarter;
        """)

        
      df["year_quarter"] = df["years"].astype(str) + " Q" + df["quarter"].astype(str)

        
      selected_years = st.sidebar.multiselect("Select Year(s):", sorted(df["years"].unique()), default=sorted(df["years"].unique()))
      selected_states = st.sidebar.multiselect("Select State(s):", sorted(df["states"].unique()), default=sorted(df["states"].unique()))

        
      filtered_df = df[df["years"].isin(selected_years) & df["states"].isin(selected_states)]

      if not filtered_df.empty:
            fig = px.bar(
                filtered_df,
                x="states",
                y="total_txns",
                color="states",
                animation_frame="year_quarter",
                title="📊 Transaction Volume by State Over Time",
                labels={"total_txns": "Total Transactions", "states": "State"},
                range_y=[0, float(filtered_df["total_txns"].max()) * 1.1],
            )
            fig.update_layout(xaxis={'categoryorder': 'total descending'}, showlegend=False)
            st.plotly_chart(fig)
      else:
            st.warning("No data available for the selected filters.")


    elif case_study == "2. Device Usage":
        st.subheader("📱 Device Usage by Region")
        df = run_query("""
            SELECT s.states, s.brands, m.total_opens
            FROM ag_user AS s
            INNER JOIN (
                SELECT states, SUM(appopens) AS total_opens
                FROM mp_user
                GROUP BY states
            ) AS m ON s.states = m.states;
        """)
        st.markdown("### 🔍 Visualization: Total App Opens by State and Brand")
        fig = px.bar(
            df,
            x='states',
            y='total_opens',
            color='brands',
            barmode='group',
            title='Total PhonePe App Opens by State and Device Brand',
            labels={'states': 'State', 'total_opens': 'Total App Opens'}
        )
        st.plotly_chart(fig)

    elif case_study == "3. Insurance Engagement":
        st.subheader("🔍 Insurance Usage by District")
        df = run_query("""
            SELECT district, SUM(transaction_count) AS txn_count
            FROM mp_insurance
            GROUP BY district
            ORDER BY txn_count DESC
            LIMIT 20;
         """)
        fig = px.bar(df, x='district', y='txn_count', title='Top 20 Districts by Insurance Transactions')
        st.plotly_chart(fig)
         
    elif case_study == "4. User Registration Analysis":
         st.subheader("📈 User Registration Trends by State Over Time")

         df = run_query("""
            SELECT states, years, quarter, SUM(registeredusers) AS total_users
            FROM top_users
            GROUP BY states, years, quarter
            ORDER BY years, quarter;
         """)

         df['time'] = df['years'].astype(str) + ' Q' + df['quarter'].astype(str)

    
         df["total_users"] = pd.to_numeric(df["total_users"], errors="coerce")
         top_states = df.groupby("states")["total_users"].sum().nlargest(10).index
         df_top = df[df["states"].isin(top_states)]

         fig = px.line(
            df_top,
            x="time",
            y="total_users",
            color="states",
            title="📊 User Registrations Over Time (Top 10 States)",
            markers=True,
            labels={"time": "Time (Year + Quarter)", "total_users": "Total Registrations"},
        )
         st.plotly_chart(fig, use_container_width=True)
         
    elif case_study == "5. Insurance Transactions Insights":
        st.subheader("🛡️ Insurance Transactions by District")
        df = run_query("""
            SELECT states, district, SUM(transaction_count) AS insurance_txns
            FROM mp_insurance
            GROUP BY states, district
            ORDER BY insurance_txns DESC
            LIMIT 20;
        """)
        fig = px.bar(df, x='district', y='insurance_txns', color='states',
                 title='Top Districts by Insurance Transaction Volume')
        st.plotly_chart(fig)



    
  
      

   


            



