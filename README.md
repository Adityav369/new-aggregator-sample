# news-aggregator-sample
This is a simple sample for web scraping in Python. The setup and run guide is given in the repository.

The project could have been improved by using:
1. Multithreading. Since the program scrapes various websites, the scraping could have been done concurrently and writing the final data could have been locked. Could have used a basic read-write monitor lock to allow multiple scrapers but only a single writer.
2. Better final delivery: The project could have been delivered in a way that is more intuitive and usable by people having a non-technical background: either by making a User interface.
3. Remove similar news: can implement an NLP algorithm to determine similarity between news and can cut out repitive news.
4. Sentiment analysis: can implement ML algorithms for news sentiment ananlysis.
5. Minor changes like reading from a email recipient list and prompting for sender email and password at runtime.

Imp Note: For the demo to actually work, please open tabular_news.py and excely_news.py and in send_email() add a sender email and password and receivers emails. If you do not want to add an email, you can also run excely_news.py to see the a new excel file being created with the latest news :)
