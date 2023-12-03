# BizCardX_Extracting-Business-Card-Data-with-OCR-Optical-Character-Recognition-

## Problem Statement
  To upload an image of a business card and extract relevant information from it using easyOCR. The extracted information should include the company name, card holder name, designation, mobile number, email address,   website URL, area, city, state,and pin code.

## Prerequisites
- `Python` programming language
- `mysql-connector-python` library
- `opencv-python` library
- `easyocr`
- `streamlit` library

  install the required libraries using pip:
   ```
   pip install easyOCR
   pip install opencv-python
   pip install streamlit
   pip install pandas 
   pip install mysql-connector-python

   ```

## MySQL Connection

1. Install MySQL Server and MySQL Workbench
2. Create a local connection and a database (business_card_data)

## How to run the application?
To run the Streamlit app, use the following command:

  ```
   streamlit run your_filename.py 
   ```

## Work Flow
Extract information from Business Card Data and store them in database

Steps involved in the application:

      * **Upload & Extract**: Users can upload a business card image and extract information from it using OCR. 
                               easyOCR is used to read the text from the image and extract information.
                               The extracted data is then stored in the MySQL database _(**business_card_data**)
                               
      * **Modify**: Users can modify the information of a specific business card stored in the database.
      
      *  **Delete**: Users can delete a specific business card from the database.
      
      *  **View all Data**: Users can view all the stored business card information in the database.
