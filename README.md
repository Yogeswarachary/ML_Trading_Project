## ML Alpha Trading Project - Yahoo Finance Data

#### About the data
- Yahoo finance is a open source trading data which is widely used ML based trading projects. This data is loaded using the **ytfinance** module available in Python libraries.
- Mostly this data was locked. everyday once or twice, we can able to access this data, otherwise this data is in locked mode. Due to this we have generated realistic data.
- If our code is unable to load the original data, then we can work on realistic data which is created with the help of Numpy cummulative sum function.

#### What this project does
- Uses machine learning to predict next‑day returns for the SPY ETF.
- Turns those predictions into trading signals (when to be in the market vs in cash).
- Evaluates the strategy with realistic metrics: Sharpe ratio, win rate, drawdown, trades per year.
- Starts from a basic long/short idea and improves it into a clean long‑only strategy with Sharpe ≈ 0.418.
- Think of it as a small “trading robot” that looks at market features every day and decides whether it is worth taking a long position in SPY or staying in cash.

#### High‑level results
- Sharpe ratio (gross): ~0.418
- Net Sharpe (after simple costs): ~0.33
- Win rate (trading days): ~55%
- Max drawdown: around −16%
- Approx. trades per year: ~27
- These numbers are for a long‑only strategy on SPY, tested out‑of‑sample on several years of daily data.
- The strategy is not meant as a guaranteed profit machine, but as a realistic, production‑style ML project that is much stronger than a typical toy example.

#### Project structure
- The project is organized into three main notebooks:
> ML_Trading_File1.ipynb – Data pipeline
  - Downloads SPY (and optionally QQQ) price data for several years.
  - Handles failures from online sources by falling back to a synthetic but realistic dataset.
  - Cleans the data and saves it as something like mltradingdata.csv.
  - Also produces quick plots of price and returns to visually inspect the data.

> Alpha_Research_File2.ipynb – Feature engineering (alpha factors)
  - Builds 19 daily features (“alpha factors”) from the market data.
  - Examples: past returns, volatility, moving averages, relative strength, etc.
  - Sets the target as “next‑day SPY return”.
  - Outputs a feature matrix of about 2,700 trading days × 19 features, saved as e.g. alpha_factors.csv.

> Production_v1.0.ipynb – Model training and trading strategy
  - Trains several models, mainly:
  - Ridge regression (baseline)
  - XGBoost regressor with time‑series cross‑validation
  - Uses proper time‑series splits (no shuffling) to avoid look‑ahead bias.
  - Tunes XGBoost hyperparameters with GridSearchCV.
  - Trains a final model on the training set and evaluates it on a held‑out test period.
  - Converts predictions into a trading strategy, computes Sharpe, win rate, drawdown, and benchmark comparisons.
  - There is also a small Streamlit dashboard and daily run setup that can read the latest results CSV and show a simple performance view.

#### Modelling approach (simple explanation)
1. Inputs (features):
- Each trading day has 19 numeric features created from recent SPY price behaviour (returns, rolling statistics, etc.).

2. Output (target):
- The target is the next‑day SPY return. The model learns patterns like:
- “When factors look like this, SPY tends to go up/down tomorrow”.

3. Models:
- Ridge regression is used as a linear baseline.
- XGBoost (gradient boosted trees) captures non‑linear relationships and interactions.
- Time‑series cross‑validation is used (e.g. 5 folds) so training only uses past data to predict future data.

4. Performance on prediction task:
- Ridge: R² around 0.18 (baseline).
- Tuned XGBoost: cross‑validated R² around 0.39–0.40, out‑of‑sample R² around 0.53 on the final test set.
- This means the model captures a meaningful part of the variation in next‑day returns, which is already quite hard in financial data.

#### Trading strategy logic
- The key idea is to only take trades when the model is relatively confident.
- After training, get the predicted next‑day return for each day.
- Compute the standard deviation of these predictions, pred_std.
- Define a threshold: threshold = 0.3 * pred_std (this “0.3×σ rule” was found to work well).
- Generate a raw long‑only signal:
- If predicted_return > threshold → go long SPY
- Otherwise → stay in cash
- Assign a position weight (for example 80% of capital) when long, 0 when out.
- Smooth the weight with an exponential moving average (EMA) so the strategy holds winners for a few days instead of flipping in and out constantly.
- Daily strategy return = (yesterday’s weight) × (today’s actual SPY return).
- From this return series, compute:
> Sharpe ratio (annualized)
> Win rate (fraction of trading days with positive strategy return when invested)
> Turnover and simple transaction cost impact
> Maximum drawdown using the cumulative equity curve.
> This long‑only, threshold‑based version significantly improved the Sharpe compared with the earlier long/short variant.

#### Backtesting and risk controls
- To keep the project realistic, several basic institutional‑style checks are included:
- Time‑series cross‑validation:
> All splits respect time order; no future data leaks into the past.
- Train/test separation:
> About 80% of the data is used for training and validation, and the last ~20% (hundreds of trading days) is kept for final out‑of‑sample evaluation.
- Simple transaction costs:
> Turnover is estimated from changes in position size; a small cost per unit of turnover is subtracted from returns to get a net Sharpe.
- Risk metrics:
> The notebook reports max drawdown and approximate number of trades per year, so the user can see how “smooth” or volatile the strategy is.
- The final configuration keeps drawdown under ~16% while preserving a positive Sharpe after costs.

#### How to run the project
- Clone the repository and open it in a Python environment (Conda/virtualenv).
- Install dependencies (typical stack: pandas, numpy, scikit‑learn, xgboost, matplotlib, yfinance, streamlit).
- Run the notebooks in this order:
> 1. ML_Trading_File1.ipynb → builds the raw market dataset.
> 2. Alpha_Research_File2.ipynb → builds 19 alpha factors.
> 3. Production_v1.0.ipynb → trains the model and runs the trading strategy.
- Optionally, run the dashboard:
- Make sure the final notebook saves the daily or aggregate results to CSV.
- Start the Streamlit app (for example: streamlit run app.py) to see the latest results and any Sharpe trends over multiple runs.
- By using Windows Task schedular and Python Papermill Module support (it auto schedules selected/saved/tasks).

Credits: Thanks to Stefen Jansan sir. I found his repository in github for Practicing the Regression based Machine Learing Project, I've taken code reference from Stefen sir repository,
and tried to increase the Sharpe value comparing with the Actual project done by the Stefen Jansan sir. Link for the Original Project Repository from Github link: https://github.com/stefan-jansen/machine-learning-for-trading
