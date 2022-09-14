# StockNews
Watch stock prices


The script checks yesterday's and the day before yesterday's end prices of the stock of a given company. If the relative difference of these consequitive days is greater
than 0.05 then it gets the latests 3 news about this company (using newsapi) and send these news in seperate messages (using twilio). 
All API keys were saved in different file.
