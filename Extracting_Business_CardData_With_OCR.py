import streamlit as st
import mysql.connector as sql
import pandas as pd
import re
import cv2
import easyocr
import numpy as np
from PIL import Image

# mysql database connection
DATABASE = "business_card_data"
mydb = sql.connect(  
    host="localhost",
    user="root",
    password="root",
    database=DATABASE
)
mycursor = mydb.cursor(buffered=True)

# create table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS card_data (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), job_title VARCHAR(255), address VARCHAR(255), postcode VARCHAR(255), phone VARCHAR(255), email VARCHAR(255), website VARCHAR(255), company_name VARCHAR(225))")
mycursor = mydb.cursor()

# import reader
reader = easyocr.Reader(['en'])

# extract information from the image using easyOCR
def extract_information(image):
    try:
        # convert PIL image to NumPy array
        image_np = np.array(image)

        # convert to grayscale (if the image is colored)
        if len(image_np.shape) == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        # Ensure the image is in binary format
        _, image_np = cv2.threshold(image_np, 128, 255, cv2.THRESH_BINARY)

        # call easyOCR
        reader = easyocr.Reader(['en'])
        results = reader.readtext(image_np)

        extracted_info = {}
        for result in results:
            text = result[1]
            if "company" in text.lower():
                extracted_info["company"] = text
            elif "name" in text.lower():
                extracted_info["name"] = text
            elif "designation" in text.lower():
                extracted_info["designation"] = text
            elif "mobile" in text.lower():
                extracted_info["mobile"] = text
            elif "email" in text.lower():
                extracted_info["email"] = text
            elif "website" in text.lower():
                extracted_info["website"] = text
            elif "area" in text.lower():
                extracted_info["area"] = text
            elif "city" in text.lower():
                extracted_info["city"] = text
            elif "state" in text.lower():
                extracted_info["state"] = text
            elif "pin" in text.lower() or "postal" in text.lower():
                extracted_info["pin_code"] = text

        return extracted_info

    except Exception as e:
        st.error(f"Exception occurred while processing the image: {e}")
        return {}

# extract information
def post_process_extracted_info(extracted_info):
    # validate and correct email using regular expression
    email_pattern = r"[^@]+@[^@]+\.[^@]+"
    if 'email' in extracted_info:
        if not re.match(email_pattern, extracted_info['email']):
            extracted_info['email'] = ""

    # validate and correct phone number using regular expression
    phone_pattern = r"\+?[0-9]+(?:[-\s()]?[0-9]+)*"
    if 'phone' in extracted_info:
        match = re.search(phone_pattern, extracted_info['phone'])
        if match:
            extracted_info['phone'] = match.group()
        else:
            extracted_info['phone'] = ""

    # validate and correct postal code using regular expression
    postal_code_pattern = r"\b\d{6}\b"
    if 'postcode' in extracted_info:
        match = re.search(postal_code_pattern, extracted_info['postcode'])
        if match:
            extracted_info['postcode'] = match.group()
        else:
            extracted_info['postcode'] = ""

    # Validate and correct website using a regular expression
    website_pattern = r"\b(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b"
    if 'website' in extracted_info:
        match = re.search(website_pattern, extracted_info['website'])
        if match:
            extracted_info['website'] = match.group()
        else:
            extracted_info['website'] = ""

    # validate and correct address using a regular expression
    address_pattern = r"(\d+\s+[A-Za-z\s]+),\s+([^,]+),\s+([^,]+),\s+(\d{6})"
    if 'address' in extracted_info:
        match = re.search(address_pattern, extracted_info['address'])
        if match:
            extracted_info['address'] = match.group(1)
            extracted_info['area'] = match.group(2)
            extracted_info['city'] = match.group(3)
            extracted_info['pin_code'] = match.group(4)
        else:
            extracted_info['address'] = ""

    return extracted_info

def delete_business_card():
    
    # creating dropdown to select business card
    mycursor.execute("SELECT name FROM card_data")
    result = mycursor.fetchall()
    business_cards = [row[0] for row in result]
    selected_card_name = st.selectbox("Select a business card to delete", business_cards)

    if selected_card_name:
        # display the current information for the selected business card
        st.write("Name:", selected_card_name)
       
        # dropdown to select business card to delete
        if st.button("Delete Business Card"):
            mycursor.execute("DELETE FROM card_data WHERE name=%s", (selected_card_name,))
            mydb.commit()
            st.success("Success! Business card information deleted from the database")
            st.balloons()
    else:
        st.warning("Error! No business card selected or card information not found in the database.")

def modify_business_card():
    # display modify content
    st.write("Modify your business card data here!")
    mycursor.execute("SELECT id, name FROM card_data")
    result = mycursor.fetchall()
    business_cards = {}
    for row in result:
        business_cards[row[1]] = row[0]
    selected_card_name = st.selectbox("Select a business card to update", list(business_cards.keys()))

    # get the current information for the selected business card
    mycursor.execute("SELECT * FROM card_data WHERE name=%s", (selected_card_name,))
    result = mycursor.fetchone()

    if result is not None:
        # display the curreninformationt  for the selected business card
        st.write("Name:", result[1])
        st.write("Job Title:", result[2])
        st.write("Address:", result[3])
        st.write("Postcode:", result[4])
        st.write("Phone:", result[5])
        st.write("Email:", result[6])
        st.write("Website:", result[7])
        st.write("company_name:", result[8])

        # get new information for the business card
        name = st.text_input("Name", result[1])
        job_title = st.text_input("Job Title", result[2])
        address = st.text_input("Address", result[3])
        postcode = st.text_input("Postcode", result[4])
        phone = st.text_input("Phone", result[5])
        email = st.text_input("Email", result[6])
        website = st.text_input("Website", result[7])
        company_name = st.text_input("Company Name", result[8])

        # create a button to update the business card
        if st.button("Update Business Card"):
            # Update the information for the selected business card in the database
            mycursor.execute(
                "UPDATE card_data SET name=%s, job_title=%s, address=%s, postcode=%s, phone=%s, email=%s, website=%s, company_name=%s WHERE name=%s",
                (name, job_title, address, postcode, phone, email, website, company_name, selected_card_name))
            mydb.commit()
            st.success("Success! Business card information updated in the database.")
            st.balloons()
    else:
        st.warning("Error! No business card selected or card information not found in the database.")

def display_database_entries():
    # display the stored business card information from the database
    mycursor.execute("SELECT * FROM card_data")
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=['id', 'name', 'job_title', 'address', 'postcode', 'phone', 'email', 'website', 'company_name'])
    st.write("Stored Business Card Information:")
    st.write(df)

def display_uploaded_business_card_info(extracted_info):
    st.write("Name:", extracted_info.get("name", ""))
    st.write("Job Title:", extracted_info.get("designation", ""))
    st.write("Address:", extracted_info.get("area", "") + extracted_info.get("city", "") + extracted_info.get("state", ""))
    st.write("Postcode:", extracted_info.get("pin_code", ""))
    st.write("Phone:", extracted_info.get("mobile", ""))
    st.write("Email:", extracted_info.get("email", ""))
    st.write("Website:", extracted_info.get("website", ""))
    st.write("Company Name:", extracted_info.get("company", ""))

# Streamlit App
def main():
    st.set_page_config(page_title="EXtracting Business Card Data With OCR", page_icon="dragon", layout="wide", initial_sidebar_state="auto")
    st.markdown("<h1 style='text-align: center; color: violet;'>EXTRACTIING BUSINESS CARD DATA WITH OCR</h1>", unsafe_allow_html=True)
    selected_option = st.selectbox("Select an option", ["Upload and Extract", "Modify", "Delete", "View all Data"])

    if selected_option == "Upload and Extract":
        # create a file uploader widget
        uploaded_file = st.file_uploader("Upload a business card image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # read the image using OpenCV
            image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
            # display the uploaded image
            st.image(image, caption='Uploaded business card image', use_column_width=True)
            
            # Create a button to extract information from the image
            if st.button('Extract Information'):
                # call the function to extract the information from the image
                bounds = reader.readtext(image, detail=0)
                # convert the extracted information
                extracted_info = {
                    'name': bounds[0],
                    'job_title': bounds[1],
                    'address': bounds[2],
                    'postcode': bounds[3],
                    'phone': bounds[4],
                    'email': bounds[5],
                    'website': bounds[6],
                    'company_name': bounds[7]
                }

                # verify extracted_info is not None before accessing its elements
                if extracted_info is not None:
                    val = (extracted_info['name'], extracted_info['job_title'], extracted_info['address'],
                           extracted_info['postcode'], extracted_info['phone'], extracted_info['email'],
                           extracted_info['website'], extracted_info['company_name'])
                else:
                    val = None
                mycursor.execute("INSERT INTO card_data (name, job_title, address, postcode, phone, email, website, company_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", val)
                mydb.commit()
                # display a success message
                st.success("Business card information added to the database.")
                # display the stored business card information
                mycursor.execute("SELECT * FROM card_data")
                result = mycursor.fetchall()
                df = pd.DataFrame(result,
                                  columns=['id', 'name', 'job_title', 'address', 'postcode', 'phone', 'email',
                                           'website',
                                           'company_name'])

                st.write(df)

    elif selected_option == "Modify":
        modify_business_card()

    elif selected_option == "Delete":
        delete_business_card()

    elif selected_option == "View all Data":
        display_database_entries()


if __name__ == "__main__":
    main()