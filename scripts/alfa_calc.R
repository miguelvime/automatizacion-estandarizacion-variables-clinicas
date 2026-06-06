
# install.packages("icr")

library(icr)

# Example data: 5 raters, 10 subjects
data<-icr::codings
alpha<-icr::krippalpha(codings, 
                metric = 'nominal',
                bootstrap = TRUE,
                bootnp = TRUE,
                cores = 4)

plot(alpha)

df <- plot(alpha, return_data = TRUE)

library(ggplot2)
ggplot() +
  geom_line(data = df[df$ci_limit == FALSE, ], aes(x, y, color = type)) +
  geom_area(data = df[df$ci == TRUE, ], aes(x, y, fill = type), alpha = 0.4) +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position = "bottom", legend.title = element_blank()) +
  ggtitle(expression(paste("Bootstrapped ", alpha))) +
  xlab("value") + ylab("density") +
  guides(fill = FALSE)
