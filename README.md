The GRADCAFE updater
====================

Automate the notification of GRADCAFE data points.

This script will fetch the result into `results` file, and
commit it with `git`. By doing so, we can send out git patch file
to our email address and view the difference quickly.

# Why?

I hate to check the website every minute, which makes me anxious and depressed.
So, I automate it and get rid of it from this stuff.


# Prerequirements

- python3
- poetry
- make


# Installation

```
$ poetry install
```

# How to Use

## Update result

Update admission result to `results`.

```
$ make update-results
poetry run python run.py > results
$ cat results
Institution: Stanford University
	 2022-03-30 00:00:00 Rejected Computer Science 2022-02-08 00:00:00

		 >> yikes

		 Rejected on 8 Feb Fall 2022 American PhD
	 2022-03-24 00:00:00 Wait Computer Science

		 >> To the MF who is spamming the results, get the f
		away. There are students whose mental health depends on this
		too. So get lost you useless clown

		 Wait listed Fall 2022 Other PhD
	 2022-03-20 00:00:00 Accepted Computer Science 2022-03-10 00:00:00
...
```

## Auto notification via mail

We can automate notification via email by usign email API service such as `mailgun`.

There is a git post-commit template in `scripts/post-commit` to help this,
after filling the required fields in the template, then copy `post-commit` into
your `.git/hooks/` directory.

After each successful commit, it will trigger this hook and send out
a git patch to your email address.


## Intergrate with crontab

Last step, we can use `crontab` to schedule it runs every x minutes.


```
* */4  * * *   <your-user-name>  cd <path-to-your-directory> && make update-results && make update
```

# Configuration

## Change fetching season

Update season in `univ.yaml` file:

```
config:
  season: F22
```

## Change fetching university

Update university entry in `univ.yaml` file:

```
univ:
  - { inst: Stanford University, degree: PhD }
  - { inst: University of Washington, degree: PhD }
  - {
      inst: "University of California, Berkeley",
      degree: Masters,
      program: Electrical Engineering And Computer Sciences,
    }
```

The fileds are:

| Name | Description |
| ---- | ----------- |
| inst | Institution, the unviersity/college name |
| degree | Degree, e.g. PhD, Master, Masters, MEng |
| program (optional) | Program name, default `Computer Science` |
