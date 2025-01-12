# Documentation: Approach for Finding "Product" URLs

## Overview
This documentation outlines the methodology and implementation used to identify and extract "product" URLs from websites using a Python-based web crawler. The approach leverages regular expressions and domain-specific patterns to dynamically filter and collect links that correspond to product-related pages.

---

## Key Steps in Identifying "Product" URLs

### 1. **Understanding Product URL Patterns**
   - Product URLs often follow consistent structures across e-commerce websites. For instance:
     - Amazon: `/dp/`, `/gp/`
     - Generic: `/product/`, `/item/`, `/view/`
     - Search Pages: `/s?k=`
   - By identifying these patterns, we can build a flexible matching system using **regular expressions**.

### 2. **Dynamic Pattern Matching**
   - A list of common product-related patterns is maintained in the code:
     ```python
     product_patterns = [
         r"/product/",
         r"/item/",
         r"/dp/",
         r"/gp/",
         r"/catalogue/",
         r"/goods/",
         r"/shop/",
         r"/view/",
         r"/detail/",
         r"/s\?k=",  # Amazon search query
     ]
     ```
   - Each pattern is a **regex** string that captures URL structures typically seen in product or e-commerce websites.
   - The `re.search()` function is used to check if a URL contains any of these patterns:
     ```python
     return any(re.search(pattern, url) for pattern in product_patterns)
     ```

### 3. **Fetching and Filtering Links**
   - **Fetching All Links**:
     - The crawler uses `BeautifulSoup` to extract all `<a>` tags containing `href` attributes from the webpage.
     - These links are normalized using `urljoin()` to ensure they are absolute URLs:
       ```python
       links = [
           urljoin(domain, a["href"])
           for a in soup.find_all("a", href=True)
           if urlparse(urljoin(domain, a["href"])).netloc in domain
       ]
       ```
   - **Filtering Product Links**:
     - Each link is evaluated using the `is_product_url()` method, which applies the regex patterns.
     - Links matching any of the product-related patterns are stored as "product URLs."

---

## How the Code Works

### Step-by-Step Explanation

1. **Initialization**:
   - The crawler initializes with a list of domains to process. 
   - A `requests.Session` is used for making HTTP requests with randomized `User-Agent` headers to avoid bot detection.

2. **Extracting Links from a Domain**:
   - For each domain:
     - The HTML content is fetched and parsed.
     - Links are extracted and normalized to ensure they belong to the same domain.

3. **Matching Product Patterns**:
   - The `is_product_url()` function checks if each link matches any of the predefined product URL patterns.

4. **Result Aggregation**:
   - Matched product URLs are collected and stored in a dictionary, where:
     - **Key**: The domain name.
     - **Value**: A list of product-related URLs.

5. **Output**:
   - The results are saved as a JSON file for further analysis or use.

---

## Example Workflow

### Input:
A domain list:
```python
domains = [
    "https://books.toscrape.com",
    "https://www.amazon.com",
    "https://scrapeme.live/shop",
]
```
## Processing

- **For `https://books.toscrape.com`**:  
  Product URLs like `/catalogue/` are matched.  

- **For `https://www.amazon.com`**:  
  Product URLs like `/dp/` or `/s?k=` are matched.  

---

## Output

A JSON file (`output.json`) with results:

```json
{
    "https://books.toscrape.com": [
        "https://books.toscrape.com/catalogue/book-1",
        "https://books.toscrape.com/catalogue/book-2"
    ],
    "https://www.amazon.com": [
        "https://www.amazon.com/dp/example-product",
        "https://www.amazon.com/s?k=search-query"
    ]
}
```

## Key Advantages of the Approach

### Dynamic Matching
- By using regex patterns, the crawler adapts to a wide variety of URL structures.

### Domain-Specific Flexibility
- Patterns can be easily expanded or customized for specific domains.

### Error Resilience
- Graceful handling of network errors or pages without product URLs.

