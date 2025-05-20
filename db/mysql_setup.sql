CREATE DATABASE IF NOT EXISTS rag_demo;
USE rag_demo;

CREATE TABLE IF NOT EXISTS federal_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_number VARCHAR(50) UNIQUE,
    title TEXT,
    summary TEXT,
    publication_date DATE,
    agency_names TEXT,
    html_url TEXT,
    pdf_url TEXT
);
