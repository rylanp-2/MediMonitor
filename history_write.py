import time


def update_history(current_led_value, last_led_value):
    global file
    with open("/static/history", "r", encoding="UTF-8") as history_file:
        file = history_file.read()
        history_file.close()

    with open("/static/history", "w", encoding="UTF-8") as history_file:
        unix = time.time()
        t = time.localtime(unix)
        formatted_time = (
            f"{t[0] % 100:02d}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"
        )

        if current_led_value == 0:
            history_file.write(f"Entered safe zone at:    {formatted_time}\n")
            history_file.write(file)
            return f"Entered safe zone at:    {formatted_time}\n"

        elif current_led_value == 1:
            history_file.write(f"Entered warning zone at: {formatted_time}\n")
            history_file.write(file)
            return f"Entered warning zone at: {formatted_time}\n"

        elif current_led_value == 2:
            history_file.write(f"Entered danger zone at:  {formatted_time}\n")
            history_file.write(file)
            return f"Entered danger zone at:  {formatted_time}\n"

    history_file.close()
