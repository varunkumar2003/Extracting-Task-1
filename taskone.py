#!/usr/bin/env python
# coding: utf-8
# In[2]
# In[4]:

import csv
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = []
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages) #reader.getNumPages()
            for page_num in range(num_pages):
                page = reader.pages[page_num] #reader.getPage(page_num)
                text.append(page.extract_text())
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text

def parse_articles(text):
    articles = []
    current_title = None
    current_body = []
    s_no = 1
    
    for line in text.split('\n'):
        if line.strip().isupper() and len(line.strip().split()) < 10:  # Assuming titles are in uppercase and less than 10 words
            if current_title:
                articles.append((s_no, current_title, " ".join(current_body).strip()))
                s_no += 1
            current_title = line.strip()
            current_body = []
        else:
            current_body.append(line.strip())
    
    if current_title:  # Append the last article
        articles.append((s_no, current_title, " ".join(current_body).strip()))
    
    return articles

def save_articles_to_csv(articles, csv_path):
    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['s_no', 'article_title', 'article_body'])
            for article in articles:
                writer.writerow(article)
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

def main(pdf_path, csv_path):
    text = extract_text_from_pdf(pdf_path)
    if text:
        full_text = " ".join(text)
        articles = parse_articles(full_text)
        save_articles_to_csv(articles, csv_path)
    else:
        print("No text extracted from the PDF.")

if __name__ == "__main__":
    pdf_path = 'visionias.pdf'  # Path to the downloaded PDF file
    csv_path = 'articles.csv'  # Path to the output CSV file
    main(pdf_path, csv_path)