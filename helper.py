from urlextract import URLExtract


def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # Number of message
    num_messages = df.shape[0]

    # Number of words
    words = []
    for message in df["message"]:
        words.extend(message.split())

    # Number of media omitetd
    num_media_messages = df[df["message"] == "<Media omitted>\n"].shape[0]

    # Number of links
    links = []
    extractor = URLExtract()

    for message in df["message"]:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    # Number of messages sent by users
    most_busy_user = df["user"].value_counts().head(5)

    # Percentage of chat
    df = round((df["user"].value_counts() / df.shape[0])*100,
               2).reset_index().rename(columns={"index": "name", "user": "percentage"})
    return most_busy_user, df
