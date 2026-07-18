function f1_calculation(true_positive, false_positive, false_negative) {
  precision <- true_positive / (true_positive + false_positive)
  recall <- true_positive / (true_positive + false_negative)
  f1_score <- 2 * ((precision * recall) / (precision + recall))
  return(f1_score)
}

