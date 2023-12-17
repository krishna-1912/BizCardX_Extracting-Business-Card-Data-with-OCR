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
* Steps involved in the application:
      *  **Upload and Extract**: Users can upload a business card image and extract information from it using OCR. The data is extracted using easyOCR and then stored in the MySQL database_(**business_card_data**)_.
      *  **Modify**: Users can modify the information of a specific business card stored in the database by selecting a specific card from dropdown.
      *  **Delete**: Users can delete a specific business card from the database by selecting a specific card from dropdown.
      *  **View all Data**: Users can view all the stored business card information in the database.

## Video Recording
https://github.com/krishna-1912/BizCardX_Extracting-Business-Card-Data-with-OCR/blob/main/EXtracting%20Business%20Card%20Data%20With%20OCR.mp4
