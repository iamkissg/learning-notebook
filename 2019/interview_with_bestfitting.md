# Interview with Bestfitting (#1 Kaggler)

> What is your first plan of action when working on a new competition?

- Create a solution document which I follow and update as the competition continues on;
- Research similar Kaggle competitions and all related papers.

> What does your iteration cycle look like?

1. Read the overview and data description of the competition carefully
2. Find similar Kaggle competitions. As a relatively new comer, I have collected and done a basic analysis of all Kaggle competitions.
3. Read solutions of similar competitions.
4. Read papers to make sure I don’t miss any progress in the field.
5. Analyze the data and build a stable CV.
6. Data pre-processing, feature engineering, model training.
7. Result analysis such as prediction distribution, error analysis, hard examples.
8. Elaborate models or design a new model based on the analysis.
9. Based on data analysis and result analysis, design models to add diversities or solve hard samples.
10. Ensemble.
11. Return to a former step if necessary.

> Favorites.

- ML algo: Prefer simple algorithms such as ridge regression when ensemble; always like starting with `resnet-50` or designing similar structure in DL competitions.
- ML lib: PyTorch in CV; TensorFlow or Keras in NLP or time-series competitions; Seaborn and products in SciPy family when doing analysis; Scikit-Learn, and XGB.

> Approach to hyper-tuning parameters.

- Try to tune parameters based on understanding of the data and the theory behind an algorithm;
- Compare the result before and after making parameter changes;
- In DL competitions, search related papers and try to find what the authors did in a similar situation.

> Approach to solid cross-validation/final submission selection and LeaderBoard fit.

- Don't go to the next step if can't find a good way to evaluate models;
- To build a stable CV, you must have a good understanding of the data and the challenges faced.
- Make sure the validation set has similar distribution to the training and test sets.
- Try to make sure models improve both on local CV and on the public LB.
- In some time-series competitions, set aside data for period of times as a validation set.
- Choose final submission in a conservative (保守的) way by always choosing a weighted average ensemble of safe models and selecting a relatively risky one (in my opinion, more parameters, more risks)
- Never choose a submission I can't explain, even with high public LB scores.

> What wins competitions?

- Good cross-validation
- Learning from other competitions
- Reading related papers
- Discipline (训练, 纪律)
- Mental toughness (坚韧)

> How important is domain expertise for you when solving data science problems?

- Don't think we can benefit from domain expertise too much:
	* Kaggle prepares the competition data carefully, and it's fair to everyone;
	* It's very hard to win a competition just by using mature methods, especially in DL competitions, we need more creative solutions;
	* The data itself is more important, although we may need read some materials related

> What do you consider your most creative trick/find/approach?

- Prepare the solution document in the very beginning and keep updating it
- The list that includes:
    * Challenges we face
    * Solutions
    * Papers need read
    * Possible risks
    * Possible cross-validation strategies
    * Possible data augmentation
    * Ways to add model diversities
- Compete in a systematic way

> What is your opinion on the trade-off between high model complexity and training/test runtime?

1. Training/test runtime is important only when it's really a problem. When accuracy is most important, model complexity should not be too much of a concern. When the training data obtained resulted from months of hard work, we must make full use of them.
2. It’s very hard to win a competition by only using ensemble of weak models now. If you want to be number 1, you often need `very good single models`. When I wanted to ensure first place in a competition solo, I often forced myself to design different models which could reach the top 10 on the LB, sometimes, even top 3. The organizers can select any one of them.
3. In my own experiences, I may design models in a competition to `explore the upper limitation of this problem`, and it’s not too difficult to then choose a simple one to make it feasible in a real situation. I always try my best to provide a simple one to organizers and discuss with them in the winner’s call. I found some organizers even use our solutions and ideas to solve other problems they face.
4. We can find that Kaggle has a lot of mechanisms to ensure the performance when the training/test runtime is important: kernel competitions, team size limitation, adding more data that aren’t calculated while scoring, etc. I am sure Kaggle will also improve the rules according to the goal of the challenge.


