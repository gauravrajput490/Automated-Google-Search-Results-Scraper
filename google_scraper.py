from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

def google_search(query, num_results=10):
    # Set up the WebDriver
    driver = webdriver.Chrome()  # Use your browser driver (e.g., ChromeDriver or GeckoDriver)
    driver.get("https://www.google.com")

    # Search for the query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(2)

    # Extract results
    results = []
    for _ in range(num_results // 10):  # Adjust for pagination
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        search_results = soup.select('.tF2Cxc')  # Google result container class
        
        for result in search_results:
            title = result.select_one('.DKV0Md').text if result.select_one('.DKV0Md') else "No Title"
            link = result.select_one('.yuRUbf a')['href'] if result.select_one('.yuRUbf a') else "No Link"
            snippet = result.select_one('.IsZvec').text if result.select_one('.IsZvec') else "No Description"
            results.append({"Title": title, "Link": link, "Description": snippet})

        # Go to the next page
        next_button = driver.find_element(By.ID, "pnnext")
        if next_button:
            next_button.click()
            time.sleep(2)
        else:
            break

    driver.quit()
    return results


def save_results_to_csv(results, filename="google_search_results.csv"):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")


if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    num_results = int(input("How many results do you want to scrape? (e.g., 10, 20): "))
    
    print("Starting Google search scraper...")
    search_results = google_search(search_query, num_results)
    
    if search_results:
        save_results_to_csv(search_results)
        print("Scraping completed!")
    else:
        print("No results found.")
