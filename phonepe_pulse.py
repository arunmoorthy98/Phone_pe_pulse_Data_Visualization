# Importing Neccessary libraries
import streamlit as st
import time
import mysql.connector
import pandas as pd
import plotly.express as px


# Setting Webpage Configurations
st.set_page_config(page_title="PhonePe", page_icon="🧭", layout="wide")

image = 'https://raw.githubusercontent.com/Sukumar9944/Phonpe-Pulse-Data-Visualization/main/Title_image/Phonepe%20Title.png'
st.image(image,width = 1050)

# MySQL Connection

connection = mysql.connector.connect(
    host = "localhost",
    port=3306,
    user = "root",
    password = 'arun1998',
    database = "phonepe_pulse")

cursor = connection.cursor()

year = [2018,2019,2020,2021,2022]
quarter = [1,2,3,4]
type = ["Transaction","User"]

select_bar1,select_bar2,select_bar3 = st.columns(3)
with select_bar1:
    Type = st.selectbox("Select the type",options = type)
with select_bar2:
    Year = st.selectbox("Select a year",options = year)
with select_bar3:
    Quarter = st.selectbox("Select a Quarter",options = quarter)

tab1, tab2, tab3 = st.tabs(["Home Page","Live Geo-Data Visualization","Top Charts Data Analysis"])

with tab1:
    st.subheader(':violet[Welcome to our PhonePe Data Analytics Dashboard!]')
    st.markdown(':green[Explore, analyze, and visualize data like never before. Uncover insights and trends that empower smarter decision-making.]')
    st.subheader(':violet[Geo_Data Visualization!]')
    st.markdown(':green[Explore dynamic geodata visualization that brings your data to life on maps. Discover geographic trends and patterns with interactive maps that provide valuable insights into your data]')
    st.subheader(':violet[Interactive Charts!]')
    st.markdown(':green[Dive into information with interactive charts that transform numbers into visual stories. From bar graphs to pie charts, explore data from different angles.]')
    st.subheader(':violet[Top Questions Answered!]')
    st.caption(':green[Get instant answers to your top questions. Our dashboard provides key insights, addressing queries on demand, so you can make informed decisions swiftly.]')



with tab2:
    if Type == "Transaction":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP - For Choropleth Map
            query1 = f'select State as State,sum(Count) as No_of_Transactions ,round(sum(Amount)) as All_Transactions , round(sum(Amount/100000000)) as Total_Payment_Value_in_Crores from map_trans where Year = {Year} and Quarter = {Quarter} group by State;'
            query2 = 'select * from states;'
            cursor.execute(query1)
            #fetch all the rows returned by the first query
            rows = cursor.fetchall()
            df1 = pd.DataFrame(rows,columns = cursor.column_names)

            cursor.execute(query2)
            rows = cursor.fetchall()
            df2 = pd.DataFrame(rows,columns=cursor.column_names)
            df1["State"] = df2

            col1,col2,col3 = st.columns(3)
            with col1:
                st.header(":blue[All Transactions]")
                total_amount = df1["All_Transactions"].sum()
                st.subheader(f':orange[{total_amount}]')
            with col2:
                st.header(":blue[No of Transactions]")
                total_transactions = df1["No_of_Transactions"].sum()
                st.subheader(f':orange[{total_transactions}]')
            with col3:
                st.header(":blue[Total payment value(Cr)]")
                InCrores = df1["Total_Payment_Value_in_Crores"].sum()
                st.subheader(f':orange[{InCrores} Cr]')
            
            # Choropleth Maps
            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations="State",
                                color = 'State',
                                color_continuous_scale='speed',
                                hover_data=['State','All_Transactions','No_of_Transactions'])

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(height=600,geo = dict(bgcolor='rgba(0,0,0,0)'))
            with st.spinner("Please wait !"):
                time.sleep(1)
            st.plotly_chart(fig,use_container_width=True)
                        


    if Type ==  "User":
        query3 = f'select State as State,sum(Registered_user) as Total_Users ,sum(App_opens) as Total_AppOpens from map_user where Year = {Year} and Quarter = {Quarter} group by State;'
        query4 = 'select * from states;'
        cursor.execute(query3)
        #fetch all the rows returned by the first query
        rows = cursor.fetchall()
        df3 = pd.DataFrame(rows,columns = cursor.column_names)

        cursor.execute(query4)
        rows = cursor.fetchall()
        df4 = pd.DataFrame(rows,columns=cursor.column_names)
        df3["State"] = df4


        st.header(":blue[Total Users]")
        total_users = df3["Total_Users"].sum()
        st.subheader(f':orange[{total_users}]')
    

    #   Choropleth Maps
        fig = px.choropleth(df3,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations="State",
                            color = 'State',
                            color_continuous_scale='speed',
                            hover_data=['State','Total_Users'])

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(height=600,geo = dict(bgcolor='rgba(0,0,0,0)'))
        with st.spinner("Please wait !"):
            time.sleep(1)
        st.plotly_chart(fig,use_container_width=True)   

with tab3:
    st.subheader(":blue[These Analysis is Based on the Overall Data]")
    questions = st.selectbox(":orange[Select any questions given below to get detailed insights:]",
    ['Click the question that you would like to query',
    '1. Top 10 states which has the highest total amount and which payment type does they belong to?',
    '2. Top 10 Brands with the most number of Registered Users?',
    '3. Which Payment Type has the highest Number of Transactions',
    '4. Average Transaction Values of each State',
    '5. Number of Registered Users present in Each Brand'])

    if questions == '1. Top 10 states which has the highest total amount and which payment type does they belong to?':
        query5 = '''select distinct(State) as State,Transaction_type,round(sum(Transaction_amount)) as Total_Transaction_amount from agg_trans
                   group by State,Transaction_type
                   order by Total_Transaction_amount desc
                   limit 10;'''
        
        cursor.execute(query5)
        rows = cursor.fetchall()
        df5 = pd.DataFrame(rows,columns=cursor.column_names)
        
        col1,col2 = st.columns(2)

        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.write(df5)
        with col2:
            # Bar Charts:
            fig = px.bar(df5,x = 'State',y = 'Total_Transaction_amount',color = 'State', title = 'Highest Total Amount by State and Payment Type')
            st.plotly_chart(fig,use_container_width=True)


    elif questions == '2. Top 10 Brands with the most number of Registered Users?':
        query6 = '''select sum(Brands) as Registered_Users,Brands as Brand from agg_user
                    group by Brand
                    order by Registered_users desc
                    limit 10;''' 
        cursor.execute(query6)
        rows = cursor.fetchall()
        df6 = pd.DataFrame(rows,columns=cursor.column_names)

        col1,col2 = st.columns(2)
        
        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.write(df6)
        with col2:
            # Bar charts:
            fig = px.bar(df6,x = "Brand",y = "Registered_Users",color = "Brand",title = 'Most Registered Users by Brand')
            st.plotly_chart(fig,use_container_width=True)

    
    elif questions == '3. Which Payment Type has the highest Number of Transactions':
        query9 = '''select Transaction_type as Transaction_type, sum(Transaction_count) as Number_of_Transactions from agg_trans
                    group by Transaction_type
                    order by Number_of_Transactions desc;'''
        cursor.execute(query9)
        rows = cursor.fetchall()
        df9 = pd.DataFrame(rows,columns = cursor.column_names)

        col1,col2 = st.columns(2)

        with st.spinner("Please wait !"):
            time.sleep(1)
        with col1:
            st.dataframe(df9)

    
    elif questions == '4. Average Transaction Values of each State':
        query12 = '''select State,round(avg(Amount))
                     as Average_Transaction_amount from map_trans
                     group by State;'''
        cursor.execute(query12)
        rows = cursor.fetchall()
        df12 = pd.DataFrame(rows,columns = cursor.column_names)
        
        with st.spinner("Please wait !"):
            time.sleep(1)
            scatter_plot = px.sunburst(df12,names = 'Average_Transaction_amount',values = 'Average_Transaction_amount',path= ['State','Average_Transaction_amount'])
            st.plotly_chart(scatter_plot,use_container_width=True)

            st.dataframe(df12)
    
    elif questions == '5. Number of Registered Users present in Each Brand':
        query13 = 'SELECT distinct(State) as State FROM agg_trans;'
        cursor.execute(query13)
        rows = cursor.fetchall()
        df13 = pd.DataFrame(rows,columns=cursor.column_names)
      
        list_of_states = df13["State"].to_dict().values()    
        State = st.selectbox("Select a State",list_of_states)

        query14 = f'''select State,sum(Count) as Registered_Users,Brands from agg_user
                     where state = '{State}'
                     group by State,Brands;'''
        
        cursor.execute(query14)
        rows = cursor.fetchall()
        df14 = pd.DataFrame(rows,columns = cursor.column_names)

        with st.spinner("Please wait !"):
            time.sleep(1)
            tree_map = px.treemap(df14,names = 'Brands',parents='State',values = 'Registered_Users',color = 'Brands',title = 'Registered Users by Brand')
            st.plotly_chart(tree_map,use_container_width=True)
            
            st.dataframe(df14)
     





