import mysql.connector
from PIL import Image, ImageDraw, ImageFont

try:
    # Connect to MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiger",
        database="CERTIFY"
    )

    # Define SQL query to fetch data for completed courses
    query = "SELECT users.name, courses.course_name, completion_records.completion_date " \
            "FROM completion_records " \
            "INNER JOIN users ON completion_records.user_id = users.id " \
            "INNER JOIN courses ON completion_records.course_id = courses.id " \
            "WHERE courses.status = 'completed'"

    # Execute SQL query
    cursor = db.cursor()
    cursor.execute(query)

    # Fetch all rows of data
    data = cursor.fetchall()

    # Close cursor and database connection
    cursor.close()
    db.close()

    # Process fetched data
    if data:
        for row in data:
            name_text, course_name, completion_date = row

            # Load the certificate image
            image = Image.open("certificate1.jpg")

            # Define coordinates for dynamic text fields
            name_coords = (405, 362, 328, 373)
            completion_coords = (305, 425, 328, 450)
            date_coords = (449, 567, 449, 569)

            # Open a drawing context
            draw = ImageDraw.Draw(image)

            # Define text and font properties
            name_font = ImageFont.truetype("arial.ttf", size=34)
            completion_font = ImageFont.truetype("arial.ttf", size=20)
            date_font = ImageFont.truetype("arial.ttf", size=24)

            # Construct completion message
            completion_text = f"{name_text} completed the course {course_name} successfully on {completion_date}"

            # Add dynamic text fields to the image
            draw.text(name_coords[:2], name_text, fill="black", font=name_font)
            draw.text(completion_coords[:2], completion_text, fill="black", font=completion_font)
            draw.text(date_coords[:2], str(completion_date), fill="black", font=date_font)  # Convert date to string

            # Save the modified image with a unique name
            image.save(f"certificate_{name_text}_{course_name}.jpg")
    else:
        print("No completed courses found.")

except mysql.connector.Error as e:
    print("MySQL Error:", e)
except IOError as e:
    print("IOError:", e)
