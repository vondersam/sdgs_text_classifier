# Multi-Label Text Classification with Transfer Learning for Policy Documents: The Case of the Sustainable Development Goals

Repository for my master thesis in Language Technology at Uppsala University.
[Link to thesis](http://uu.diva-portal.org/smash/record.jsf?pid=diva2%3A1360968&dswid=-5478)

## Abstract

We created and analyzed a text classification dataset from freely-available web documents from the United Nation's Sustainable Development Goals. We then used it to train and compare different multi-label text classifiers with the aim of exploring the alternatives for methods that facilitate the search of information of this type of documents.

We explored the effectiveness of deep learning and transfer learning in text classification by fine-tuning different pre-trained language representations — Word2Vec, GloVe, ELMo, ULMFiT and BERT. We also compared these approaches against a baseline of more traditional algorithms without using transfer learning. More specifically, we used multinomial Naive Bayes, logistic regression, k-nearest neighbors and Support Vector Machines.

We then analyzed the results of our experiments quantitatively and qualitatively. The best results in terms of micro-averaged F1 scores and AUROC are obtained by BERT. However, it is also interesting that the second best classifier in terms of micro-averaged F1 scores is the Support Vector Machines, closely followed by the logistic regression classifier, which both have the advantage of being less computationally expensive than BERT. The results also show a close relation between our dataset size and the effectiveness of the classifiers.

## Repository modules

* **Label_extract** contains the code used to create and label the dataset from documents scraped with Scrapy (whose script is not publicly available).
* **Experiments** contains all the experimental Jupyter notebooks, which includes:
  
  * Data analysis of the dataset
  * K-fold splitting of the data
  * Multi-label text classification experiments with Multinomial Naive Bayes, k-NN, SVM, Logistic Regression, Word2Vec, GloVe, ELMo, ULMFiT and BERT

## How to cite
```
@Misc{multi_label_sdgs,
  author        = {Rodríguez Medina, Samuel},
  title         = {Multi-Label Text Classification with Transfer Learning for Policy Documents: The Case of the Sustainable Development Goals},
  year          = {2019},
  url           = {http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-395186},
}
```
