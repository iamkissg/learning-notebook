# Visualizing memorization in RNNs

> Inspecting gradient magnitudes in context can be a powerful tool to see when recurrent units use short-term or long-term contextual understanding. (第一张是如何实现的, 存疑, attention?)

- **Recurrent Unit, Nested LSTM:** makes the cell update depend on another LSTM unit, supposedly this allows more long-term memory compared to stacking LSTM layers.
- **Recurrent Unit, LSTM:** allows for long-term memorization by gating its update, thereby solving the vanishing gradient problem.
- **Recurrent Unit, GRU:** solves the vanishing gradient problem without depending on an internal memory state.

> Differences in high-level quantitative measures can have many explanations and may only be because of some small improvement in predictions that only requires short-term contextual understanding, while it is often the long-term contextual understanding that is interest. Thus, comparing different Recurrent Units is often more involved than simply comparing the accuracy or cross entropy loss.

- To get a better idea of how well each model memorizes and uses memory for contextual understanding, the connectivity between the desired output and the input is analyzed. (为了更好地理解模型记忆, 考察输入与输出之间的联系, 考虑模型对于上下文记忆与理解的能力)

![LSTM model in this setup is capable of long-term memorization, but not long-term contextual understanding.](/home/kissg/Developing/learning-notebook/2019/img/long-term_memorization_is_not_long-term_understanding.png)

- 这个例子很有意思, LSTM 几乎记住了所有之前的内容, 但是它的预测差了十万八千里. 这说明, 此处的 LSTM 模型具有长期记忆, 但不具备长期上下文理解能力.
- 就单词自动补全模型而言, 短期上下文理解通常发生在被预测的单词本身中, 即模型从关注之前的单词转向关注自身的字母. 刚在新单词的伊始, 模型更关注之前的单词.

![Autocomplete accuracy graph](/home/kissg/Developing/learning-notebook/2019/img/autocomplete_accuracy_graph.png)

- 本文的实验, GRU 更擅长长期上下文理解, 而 LSTM 更擅长短期上下文理解.
- In this case, the connectivity visualization together with the autocomplete predictions, reveals that the GRU model is much more capable of long-term contextual understanding, compared to LSTM and Nested LSTM.