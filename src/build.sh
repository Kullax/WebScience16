# Edit the output and the fold name
java -cp "*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -sentimentModel edu/stanford/nlp/models/sentiment/sentiment.ser.gz -input ../fold1.txt > output.txt