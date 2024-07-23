# Predicting Christmas Spending

Back in December 2023, I wanted to predict how much Americans would spend on Christmas gifts prior to the release by the National Retail Federation. Prior to release, it seemed that it was on an upward trajectory:

![Imgur](https://i.imgur.com/RVqpjZc.png)

As we can see, with year as a predictor, the trend seems nonlinear, even on a log scale. So, there are many different approaches we can take. This post documents each approach I took, evaulating how each performed back when I wrote them, and then seeing how they each did knowing now how much Americans spent.

## Models

I figured with year as a predictor, it would be best to use time-series models. However, the growth over time could instead be modeled as a function of several predictors, of which the growth is derived from. So, I decided a good place to start was a simple linear regression model, alongside its Bayesian counterpart, as well as two timer series models: one that deals only with observed values and another that takes into account predictors. Each will be covered in depth.

## Predictors

For predictors, I chose the following based on some preliminary research (and by that, I mean my basic knowledge of economics paired with some online articles):

- US GDP per year
- US Population per year
- Median income
- Unemployment rate
- Consumer Confidence Index
- Interest Rate
- Inflation Rate
- Real estate market

From these predictors, it was found that leaving them untransformed provided by thest preliminary correlation (this may have been a bad decision on my part, as my search was not exhaustive). This leaves us with the following:

![Imgur](https://i.imgur.com/w7LDC5e.png)

However, in examining the predictors, I noted some co-linearity via a heatmap:

![Imgur](https://i.imgur.com/hyu1FAR.png)

So, we also examine the use of PCA in our OLS model.

## Prediction

### OLS

First, we attempt to use some baseline linear regression on the raw data. Quick reminder that OLS assumes:

$$Y|X \sim N(\beta X, \sigma^2)$$

for some estimated \\( \sigma^2 \\). The results:

| Model                      |   R-Squared |    MSE |   Predicted Value |   Lower Bound |   Upper Bound |
|:---------------------------|------------:|-------:|------------------:|--------------:|--------------:|
| Linear Regression, non-PCA |        0.99 | 370.67 |            890.06 |        838.64 |        941.49 |
| Linear Regression, PCA     |        0.96 | 863.65 |            891.76 |        754.64 |       1028.87 |

As expected, the PCA model has higher MSE and lower R-squared, but it generalizes well it seems with a higher predictive value for the trend. It also results in a wider 95\% CI, and it seems that both predict far less than what might be expected from the trend.

### Bayesian Linear Regression
Bayesian Linear Regression has a similar set-up, with:

$$Y|X, \beta \sim N(\beta X, \sigma^2) $$

But we also assume priors on these values. Typically, we would use noninformative priors, but using pymc, we can better use already existing distributions. That is, we allow priors of:

$$\sigma^2 \sim C$$
$$\beta_0 \sim N(\hat\beta_0, 1)$$
$$\beta_{1:p} \sim N(\hat\beta_{1:p}, I)$$

Since we know that, under noninformative priors, our posterior should have a center similar to the OLS prediction.

Running this setup on 4 chains gives us convergence on all chains for each dsitribution,

![Imgur](https://i.imgur.com/nGM2cpq.png)

So, a slightly lower value than OLS (which is usual, since Bayesian estimates tend to provide more conservative estimates compared to its OLS counterpart as a result of the priors)

### ARIMA and SARIMAX
Next, we make use of Auto-Regressive Integrated Moving Average models, are ARIMA for short. These models combine 3 separate practices that are usual in time series:

- Auto-Regressive principals (each future point is a function of some set of the previous)
- Moving Average (each point is a linear addition)
- Integrated (we assume that in our Auto-Regressive part, there is some unit root of a given finite multiplicity that can be factored out, providing a baseline for our predictions).

From playing around with the data and convergence, I found that I got the best results with ARIMA(3, 3, 3), meaning taking a look at the past 3 points and using iid shocks to represent differences, as well as also viewing roots of size 3. This is represented as:

$$\left(1 - \sum_{i=1}^3(1-\phi_i L^i)\right) (1-L)^3 Y_t = \left(1 + \sum_{i=1}^3 \theta_i L^i\right) \epsilon_t$$

Where "L" is what is called the "Lag operator".

Ex:

$$L Y_t = Y_{t - 1}$$

$$L^2 Y_t = Y_{t - 2}$$

When expanded out, we get that:

$$Y_t = f(Y_{t-1}, Y_{t-2}, Y_{t-3}, \theta_{t-1}, \theta_{t-2}, \theta_{t-3}, \phi_{t-1}, \phi_{t-2}, \phi_{t-3})$$

And we can use a log-likelihood maximizer to find the best predictions.

This is great, but what if we also want to include some of our linear predictors like before? Well, for this, we have to use a Seasonal Auto-Regressive Integrated Moving Average with Exogeneous Regressors (SARIMAX). Now, to be completely honest, I only understand this to a baseline, but essentially (assuming no seasonality), this ends up being a simila result to ARIMA with the introduction of predictors on \\( X_t \\). So, it will be:

$$Y_t = f(Y_{t-1}, Y_{t-2}, Y_{t-3}, \theta_{t-1}, \theta_{t-2}, \theta_{t-3}, \phi_{t-1}, \phi_{t-2}, \phi_{t-3}, \boldsymbol{\beta}, X_t)$$

Running both, we get some interesting results:

| Name    |    Mean |   Lower Bound |   Upper Bound |
|:--------|--------:|--------------:|--------------:|
| ARIMA   | 963.957 |       928.775 |       999.138 |
| SARIMAX | 971.21  |       960.691 |       981.728 |

We get much more realistic predictions and not only that, we get even tighter bounds. We can already hypothesize that this will be the best model, but let's see how all of them did.

### Results

Spending ended up being **$964.4 billion**.

Comparing each result, it is clear that ARIMA did the best by far on predicting 2023 spending. Plotting with 95\% confidence intervals (or for the Bayesian Linear Regression, credible interval)

![Imgur](https://i.imgur.com/FSJyh3e.png)

And looking at the residuals:

![Imgur](https://i.imgur.com/Rq7C5xK.png)

ARIMA did the best by far, getting within 0.5 of the true value. Does this mean that it is better than SARIMAX? Maybe not: it could be that for last year, it just proved to be a better estimate, but it may not be that way continuing on. That being said, if we want to predict next year's spending, it is much easier to predict using ARIMA.

## Conclusions and Next Year's Prediction

Running the ARIMA model again, we get that for next year, we can possibly get the first year that American Christmas spending surpasses $1 trillion.

- Predicted value: $1.026 trillion
- CI: $992 billion to $1.059 trillion