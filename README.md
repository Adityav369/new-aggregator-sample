# news-aggregator-sample
This is a simplistic sample of the news aggregator I implemented for CLSA. The setup and run guide is given in the repository. The project only has 1 news website and 1 market sector. It was used to train employees in basic web scraping and data processing using python to help further the automation efforts at the firm. The comprehensive project is the property of the organization and cannot be shared online. It includes multiple sectores, and multiple news websites.

The project could have been improved by using:
1. Multithreading. Since the program scrapes various websites, the scraping could have been done concurrently and writing the final data could have been locked. Could have used a basic read-write monitor lock to allow multiple scrapers but only a single writer.
2. Better final delivery: The project could have been delivered in a way that is more intuitive and usable by people having a non-technical background.
3. Sentiment analysis: can implement ML algorithms for news sentiment ananlysis.
