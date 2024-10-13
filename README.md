# Candoosms Scrapy Project

This project is a Scrapy-based web crawler designed to extract data from `my.candoosms.com`, specifically from the message sendbox section. The crawler fetches pages of outbound SMS messages, processes them, and outputs the data in CSV format.

## URL Templates for Data

The crawler retrieves paginated data from the following URL template:

```
https://my.candoosms.com/ms-sendbox-o?useajax=true&rand=<RANDOM_VALUE>&fid=&page=<PAGE_NUMBER>&order=outbound_message_id:DESC&filter=
```

### Example:

```
https://my.candoosms.com/ms-sendbox-o?useajax=true&rand=h0de80bdatj52kimnnuqn3jt96&fid=&page=2&order=outbound_message_id:DESC&filter=
```

- **`rand`**: A dynamic value that is extracted from the page.
- **`page`**: The page number to fetch data from.

## Commands to Execute the Program

### Running the Scrapy Spider

You can run the Scrapy spider using the command-line interface (CLI). You need to provide the necessary arguments, including the session cookie and the page range you want to scrape.

```bash
scrapy crawl candoosms -a cookie=<YOUR_COOKIE> -a s=<START_PAGE> -a e=<END_PAGE>
```

#### Example:

```bash
scrapy crawl candoosms -a cookie=vtlv44nhdbbg6rij3kfob6vr23 -a s=1 -a e=10
```

- **`cookie`**: The PHP session ID obtained from the browser after logging into the site.
- **`s`**: Start page number.
- **`e`**: End page number.

### Running the Executable (.exe) File

If you want to run the project as a standalone executable (without needing to install Python or Scrapy), you can use the `.exe` file created using **PyInstaller**. 

To run the executable, pass the cookie value along with the page range as arguments:

```bash
candoosms.exe <COOKIE> <START_PAGE> <END_PAGE>
```

#### Example:

```bash
candoosms.exe h0de80bdatj52kimnnuqn3jt96 1 5
```

### Creating the Executable File

You can create an `.exe` file for this Scrapy project using **PyInstaller**. To do this, navigate to the project directory and run the following command:

```bash
pyinstaller --onefile .\candoosms\spiders\candoosms.py
```


This will generate a standalone executable in the `dist` directory.

## Retrieving the Cookie Value

To run the crawler, you'll need to pass a session cookie (`PHPSESSID`) from the `my.candoosms.com` website. Here's how to retrieve it:

1. **Login to `my.candoosms.com`:** Open the browser, navigate to the login page, and log in using your credentials.
2. **Solve CAPTCHA**: After logging in, ensure that the CAPTCHA is correctly solved.
3. **Extract the `PHPSESSID` cookie**: Open the browser developer tools (F12), go to the "Application" or "Storage" tab, and look for the `PHPSESSID` cookie under the Cookies section for the `my.candoosms.com` domain.

Once you have the `PHPSESSID` value, use it in the commands as shown above.

---

By following these instructions, you'll be able to scrape data from `my.candoosms.com` and create standalone executables for easier distribution and execution of the crawler.
