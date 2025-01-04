# STKI Backend

Repository ini adalah backend dan API menggunakan Flask yang mengambil berita dari dataset yang disimpan dalam file CSV.

## Cara install

1. Clone repository

2. Install dependency

   ```
   pip install -r requirements.txt
   ```

3. Download dataset dari https://www.kaggle.com/datasets/iqbalmaulana/indonesian-news-dataset dan pindahkan file CSV ke `data/data.csv`

4. Jalankan aplikasi Flask

   ```
   python app.py
   ```

5. Akses API di `http://127.0.0.1:5000/news?page=1` untuk mendapatkan halaman pertama dari berita

## Pagination

API mendukung pagination, memperbolehkan mengambil 10 berita dalam satu halaman. Anda bisa menentukan nomor halaman dengan query string, misal `?page=2` untuk halaman kedua.

# Search Engine Project

This project is a simple search engine built using Flask and the Whoosh library. It allows users to search for specific keywords, words, or phrases in indexed documents.

## Project Structure

```
search-engine-project
├── src
│   ├── app.py          # Entry point of the application
│   ├── search.py       # Logic for indexing and searching documents
│   └── templates
│       └── index.html  # HTML template for the search interface
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd search-engine-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/app.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:5000` to access the search interface.

## Usage Guidelines

- Enter your search keywords in the provided input field and submit the form to see the search results.
- The search engine will return documents that match your query based on the indexed content.

## License

This project is licensed under the MIT License.