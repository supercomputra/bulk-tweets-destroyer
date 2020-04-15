## Get Started

### 1. Download Your Twitter Data
Download your Twitter Data https://twitter.com/settings/your_twitter_data

### 2. Prepare Data as JSON file in The Directory
Unarchive your twitter data and move the `data/tweet.js` file containing all tweet to the directory. Format the file as JSON file by removing `window.YTD.tweet.part0 = ` in the first line and save the file as `data.json`.

### 3. Set Up Twitter Developer Account
Create your own app in twitter https://developer.twitter.com/en/apps/create and get all the keys below:
- Consumer key
- Consumer secret key
- Access token key
- Access token secret key

### 4. Execute The Script
In the terminal execute this line
```
python destroyer.py --date 2020-04-14 -k [CONSUMER_API_KEY] -s [CONSUMER_API_KEY_SECRET] --token-key [ACCESS_TOKEN_KEY] --token-secret [ACCESS_TOKEN_SECRET]
```

#### Arguments
```
  -d DATE, --date DATE          Delete tweets until this date with format 2020-04-14
  -k KEY, --key KEY             Consumer API key
  -s SECRET, --secret SECRET    Consumer API secret key
  --token-key TOKEN_KEY         Access token key
  --token-secret TOKEN_SECRET   Access token secret
  ```
