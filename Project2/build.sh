# Edit the output and the fold name
cd stanford-corenlp-full-2015-12-09
java -cp "*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -sentimentModel edu/stanford/nlp/models/sentiment/sentiment.ser.gz -input ../ReadyForStanford.txt > output.txt