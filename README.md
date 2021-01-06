# american_literature
- crawl, processing code
- https://americanliterature.com/short-746story-library,

![](ALSS_web.png)

Splicing all the articles into sentences with spaCy takes almost a day. This resulted in a total of 1.148 million sentences. 
 
We connected the consecutive sentence one by one to make the sentence to sentence prediction form of the dataset avoiding the last sentence of a story connected to the start of the other story article. 
Then those dataset examples were split into 8:1:1 ratio to make train, dev, and test set. 
After that, we filtered outliers amongst the sentences that are too lengthy (more than 70 tokens) or short (less than 3 tokens) 
which results in 11.98\% (train/val/test $=$ 11.99\%, 11.99\%, 11.90\%) excluded sentences.
