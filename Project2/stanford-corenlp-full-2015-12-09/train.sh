cd stanford-corenlp-full-2015-12-09
# can be run after having constructed a tree file, from googledocs.py script
# and having run build.sh script.
java -cp "*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath ../non_senti/train0.txt -epochs 3 -train -model non_sem_fold0.ser.gz -nthreads 8
java -cp "*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath ../non_senti/train1.txt -epochs 3 -train -model non_sem_fold1.ser.gz -nthreads 8
java -cp "*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath ../non_senti/train2.txt -epochs 3 -train -model non_sem_fold2.ser.gz -nthreads 8
# now fold it like it's hot cookie dough
java -cp "*" edu.stanford.nlp.sentiment.Evaluate -model non_sem_fold0.ser.gz -treebank ../non_senti/test0.txt &> fold0.non
java -cp "*" edu.stanford.nlp.sentiment.Evaluate -model non_sem_fold1.ser.gz -treebank ../non_senti/test1.txt &> fold1.non
java -cp "*" edu.stanford.nlp.sentiment.Evaluate -model non_sem_fold2.ser.gz -treebank ../non_senti/test2.txt &> fold2.non


# can be run after having constructed a tree file, from googledocs.py script
# and having run build.sh script.
java -cp "*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath ../senti/train0.txt -epochs 3 -train -model sem_fold0.ser.gz -nthreads 8
java -cp "*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath ../senti/train1.txt -epochs 3 -train -model sem_fold1.ser.gz -nthreads 8
java -cp "*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath ../senti/train2.txt -epochs 3 -train -model sem_fold2.ser.gz -nthreads 8
# now fold it like it's hot cookie dough
java -cp "*" edu.stanford.nlp.sentiment.Evaluate -model sem_fold0.ser.gz -treebank ../senti/test0.txt &> fold0.sem
java -cp "*" edu.stanford.nlp.sentiment.Evaluate -model sem_fold1.ser.gz -treebank ../senti/test1.txt &> fold1.sem
java -cp "*" edu.stanford.nlp.sentiment.Evaluate -model sem_fold2.ser.gz -treebank ../senti/test2.txt &> fold2.sem
cd ..