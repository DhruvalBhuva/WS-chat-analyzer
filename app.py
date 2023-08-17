import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # To convert to a string based IO:
    data = bytes_data.decode("utf-8")
    # st.text(data)

    df = preprocessor.proprocess(data)

    st.dataframe(df)

    # Fetch Unique Users
    unique_users = df["user"].unique().tolist()
    unique_users.remove("group_notification")
    unique_users.sort()
    unique_users.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis of:", unique_users)

    if st.sidebar.button("Show Analysis"):

        # ''' Stats area for group and solo user '''

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(
            selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.info("Total Messages")
            st.write(num_messages)

        with col2:
            st.info("Total Words")
            st.write(words)

        with col3:
            st.info("Media Shared")
            st.write(num_media_messages)

        with col4:
            st.info("Links Shared")
            st.write(num_links)

        # ''' Finding the busiest users area for group only '''

        if selected_user == "Overall":
            st.info("Busiest Users")
            col1, col2 = st.columns(2)

            most_busy_user, nuw_df = helper.most_busy_users(df)

            fig, ax = plt.subplots()

            with col1:
                ax.bar(most_busy_user.index, most_busy_user.values)
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                st.info("Percentage of messages sent")
                st.dataframe(nuw_df)
