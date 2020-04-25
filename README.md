# Chr0m1ng Twitter Bot

This bot will **read all my tweets** and at some point
will **create a tweet** using **Markov Chains** technique.

## Architecture draft

To achieve the goal of this project it's necessary a database,
since I'll use `python` I chose `MongoDB`.

I'll use `Twitter` API to get all my tweets and
create a `Markov Chain` to genarate a new tweet.

### MongoDB

At `MongoDB` I'll have 3 `collections`:
| Collection | Description    |
|:-----------|:---------------|
| tweets     | My own tweets  |
| bot_tweets | Bot tweets     |
| chains     | Created chains |

### Twitter

With the `Twitter` API I'll do basically 3 things:

- Get all my old tweets and save to `MongoDB`;
- Get my new tweets via `Stream` and save to `MongoDB`;
- Post a tweet.

### Markov Chain

#### Creating chain

In order to generate a new tweet I'll create a `Markov Chain`.

To every tweet I'll do the following steps:

- Split the tweet in words;
- Remove punctuation chars;
- Add it to a `list` of tweets.

After I organize my tweets in a `list` of **clean word-tweets** I need to
iterate over this `list` to fill the following `dict`:

- every word => `dict` where:
    - `nodes` => `dict` where:
        - following word => `dict` where:
            - `n_occurr` => number of occurrences;
            - `r_occurr` => rate of occurrences;
            - `w_type` => `dict` where:
                - `n_mid` => number of mid occurrences;
                - `r_mid` => rate of mid occurrences;
                - `n_end` => number of end occurrences;
                - `r_end` => rate of end occurrences.
    - `is_init` => `boolean`.

Example:
Imagine the following tweet:

```text
Sometimes I'll start a sentence, and I don't even know where it's going.
I just hope I find it along the way. Like an improv conversation. An improversation.
```

This would turn into something like:

```json
{
  "Sometimes": {
    "nodes": {
      "I'll": {
        "n_occurr": 1,
        "w_type": {
            "n_mid": 1,
            "n_end": 0
        }
      }
    },
    "is_init": true
  },
  ...
  "I": {
    "nodes": {
      "don't": {
        "n_occurr": 1,
        "w_type": {
            "n_mid": 1,
            "n_end": 0
        }
      },
      "just": {
        "n_occurr": 1,
        "w_type": {
            "n_mid": 1,
            "n_end": 0
        }
      },
      "find": {
        "n_occurr": 1,
        "w_type": {
            "n_mid": 1,
            "n_end": 0
        }
      }
    },
    "is_init": false
  },
  ...
  "An": {
    "nodes": {
      "improversation": {
        "n_occurr": 1,
        "w_type": {
            "n_mid": 0,
            "n_end": 1
        }
      }
    },
    "is_init": false
  },
  "improversation": {
    "nodes": {},
    "is_init": false
  }
}

```

In order to populate the above `dict` I'll follow some rules
while iterating the `list`:

- If the current word **isn't** a `dict` `key`:
    - create the `key`.
- If the current word **is** the first word:
    - set `is_init` as `true`.
- If the current word **isn't** the first word:
    - set `is_init` as `false`.
- If the current word **isn't** the last word:
    - get the following word;
    - if this word **isn't** a `dict` `key` of the current word `nodes` `dict`:
        - create the `key` at `nodes`.
    - increase the `n_occurr` of this word.
    - if this word **isn't** the last word:
        - increase the `w_type.n_mid` of this word.
    - if this word **is** the last word:
        - increase the `w_type.n_end` of this word.

After the first population I need to iterate over every word's `nodes`
and calculate `r_occurr`, `r_mid` and `r_end`.

Ps.: The rate it's just a simple average.

#### Generating tweet

With the `Markov Chain` created I can now generate a new tweet,
to do so I will follow some steps:

- Chose a word where `is_init` is `true`;
- Start a tweet with that word;
- Until I find an **end word** or the **tweet length** exceed I will:
    - chose a word from current word's `chains`
    using `r_occurr` `keys` as probability values;
    - append this word to the tweet;
    - chose if this word is an end or mid word using `w_type.r_mid`
    and `w_type.r_end` as probability values.

---

## Harvest

For the first run I need to fill the `MongoDB` `tweets` collection at with some tweets.

To do so, I'm going to use the `get user timeline` via Twitter API
to get all my old tweets.

Now that I have my old tweets I just need to save them to `MongoDB` `tweets` collection.

---

## Stream

The app will fetch tweets via Twitter API streaming option and
for every new tweet will do the following steps:

- Check if this tweet is a bot tweet using the `tweet.id` and
the stored `bot_tweets` collection from `MongoDB`;
- If it **isn't** a bot tweet:
    - save the tweet to `MongoDB` `tweets` collection.

---

## Bot's routine

- Woke up with some trigger **TBD**;
- Get all tweets from `MongoDB` `tweets` collection;
- Create a new `Markvo Chain`;
- Save the `Chain` to `MongoDB` `chains` collection;
- Generate a tweet with that `Chain`;
- Post the tweet;
- Create a `dict` where:
    - `tweet` => the generated tweet text;
    - `id` => `tweet.id`.
- Save this `dict` to `MongoDB` `bot_tweets` collection.
- Lay down and wait.
