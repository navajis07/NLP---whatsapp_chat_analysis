import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s'

    full_message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Split Date and Time
    date = []
    times = []
    for i in dates:
        date.append(i.split(", ")[0])
        times.append(i.split(", ")[1])

    time = []
    for i in times:
        time.append(i.split()[0])  # Using regular space as separator

    # Create DataFrame¶
    df = pd.DataFrame({
        'user_message': full_message,
        'date': date,
        'time': time
    })

    # Spliting user name and msg
    users = []
    messages = []
    for i in df['user_message']:
        x = re.split("([\w\W]+?):\s", i)
        if x[1:]:  # user name
            users.append(x[1])
            messages.append(x[2])
        else:
            users.append('Group Notification')
            messages.append(x[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Convert Date Column into DateTime format
    df["date"] = pd.to_datetime(df['date'])

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df







    # df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # # convert message_date type
    # # df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    # df['message_date'] = pd.to_datetime(df['message_date'], errors='coerce')
    #
    # df.rename(columns={'message_date': 'date'}, inplace=True)
    #
    # users = []
    # messages = []
    # for message in df['user_message']:
    #     entry = re.split('([\w\W]+?):\s', message)
    #     if entry[1:]:  # user name
    #         users.append(entry[1])
    #         messages.append(" ".join(entry[2:]))
    #     else:
    #         users.append('group_notification')
    #         messages.append(entry[0])
    #
    # df['user'] = users
    # df['message'] = messages
    # df.drop(columns=['user_message'], inplace=True)
    #
    # df['only_date'] = df['date'].dt.date
    # df['year'] = df['date'].dt.year
    # df['month_num'] = df['date'].dt.month
    # df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day
    # df['day_name'] = df['date'].dt.day_name()
    # df['hour'] = df['date'].dt.hour
    # df['minute'] = df['date'].dt.minute
    #
    # period = []
    # for hour in df[['day_name', 'hour']]['hour']:
    #     if hour == 23:
    #         period.append(str(hour) + "-" + str('00'))
    #     elif hour == 0:
    #         period.append(str('00') + "-" + str(hour + 1))
    #     else:
    #         period.append(str(hour) + "-" + str(hour + 1))
    #
    # df['period'] = period
    #
    # return df